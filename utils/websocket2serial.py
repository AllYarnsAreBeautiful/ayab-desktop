import serial
import asyncio
import websockets
import websockets.exceptions
import logging
import socket
import argparse
import contextlib
from zeroconf.asyncio import (
    AsyncServiceInfo,
    AsyncZeroconf,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Serial Port Configuration (set via command-line arguments) ---
SERIAL_PORT = "/dev/ttyUSB0"
SERIAL_BAUD_RATE = 115200
SERIAL_TIMEOUT = 0.1

# --- WebSocket Configuration ---
WEBSOCKET_HOST = "0.0.0.0"  # Listen on all available interfaces
WEBSOCKET_PORT = 8080
WEBSOCKET_PATH = "/ws"

# --- Zeroconf Configuration ---
ZEROCONF_SERVICE_TYPE = "_ayab._tcp.local."
ZEROCONF_SERVICE_NAME = "Ayab Serial Bridge"

# Global variables for Zeroconf instance and service info
zeroconf_instance = None
service_info = None
serial_port_lock = asyncio.Lock()


async def serial_to_websocket_task(serial_port_name, websocket, ser):
    """
    Asynchronously reads data from the serial port and sends it to the
    WebSocket. This task runs continuously as long as the WebSocket
    connection is open.
    """
    logging.info(
        f"Starting serial_to_websocket_task for {serial_port_name}"
        f"(WS client: {websocket.remote_address})"
    )
    try:
        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)  # Read all available data
                logging.debug(
                    f"Serial -> WS: Read {len(data)} bytes from "
                    f"{serial_port_name}: {data!r}"
                )
                try:
                    await websocket.send(data)  # Send raw binary data
                    logging.debug(f"Serial -> WS: Sent {len(data)} bytes to WS client.")
                except websockets.exceptions.ConnectionClosedOK:
                    logging.info(
                        f"Serial -> WS: WebSocket client "
                        f"{websocket.remote_address} disconnected cleanly."
                    )
                    break  # Exit task if client disconnects
                except Exception as e:
                    logging.exception(
                        f"Serial -> WS: Error sending data to WebSocket: {e}"
                    )
                    break  # Exit task on other WebSocket errors
            await asyncio.sleep(SERIAL_TIMEOUT)
    except Exception as e:
        logging.exception(f"Serial -> WS task encountered an unexpected error: {e}")
    finally:
        logging.info(
            f"Stopped serial_to_websocket_task for {serial_port_name} "
            f"(WS client: {websocket.remote_address})"
        )


async def websocket_to_serial_task(serial_port_name, websocket, ser):
    """
    Asynchronously receives data from the WebSocket and sends it to the
    serial port. This task runs continuously as long as the WebSocket
    connection is open.
    """
    logging.info(
        f"Starting websocket_to_serial_task for {serial_port_name} "
        f"(WS client: {websocket.remote_address})"
    )
    try:
        while True:
            try:
                # Receive data from WebSocket. 'await websocket.recv()' is blocking.
                # It will wait until data is received or connection is closed.
                message = await websocket.recv()
                logging.debug(
                    f"WS -> Serial: Received {len(message)} bytes from "
                    f"WS client: {message!r}"
                )

                if isinstance(message, bytes):
                    ser.write(message)
                    logging.debug(
                        f"WS -> Serial: Wrote {len(message)} bytes to "
                        f"{serial_port_name}."
                    )
                else:
                    logging.warning(
                        f"WS -> Serial: Received non-binary message "
                        f"(type: {type(message)}), discarding: {message!r}"
                    )

            except websockets.exceptions.ConnectionClosedOK:
                logging.info(
                    f"WS -> Serial: WebSocket client "
                    f"{websocket.remote_address} disconnected cleanly."
                )
                break  # Exit task if client disconnects
            except websockets.exceptions.ConnectionClosed as e:
                logging.warning(
                    f"WS -> Serial: WebSocket connection closed unexpectedly: {e}"
                )
                break  # Exit task on unexpected connection closure
            except Exception as e:
                logging.exception(
                    f"WS -> Serial: Error receiving from WebSocket or "
                    f"writing to serial: {e}"
                )
                break  # Exit task on other errors
    except Exception as e:
        logging.exception(f"WS -> Serial task encountered an unexpected error: {e}")
    finally:
        logging.info(
            f"Stopped websocket_to_serial_task for {serial_port_name} "
            f"(WS client: {websocket.remote_address})"
        )


async def serial_websocket_handler(serial_port_name, baud_rate, websocket):
    """
    Main handler for each new WebSocket connection.
    It opens the serial port and creates two tasks for bidirectional
    communication.
    """
    global serial_port_lock

    if websocket.request.path != WEBSOCKET_PATH:
        error_message = (
            f"Error: No handler for path {websocket.request.path}, "
            f"closing connection"
        )
        await websocket.send(error_message)
        logging.error(error_message)
        return

    if serial_port_lock.locked():
        error_message = (
            f"Error: Serial port {serial_port_name} is already in use by "
            f"another connection."
        )
        await websocket.send(error_message)
        logging.error(error_message)
        return

    logging.info(
        f"New WebSocket connection from {websocket.remote_address}. "
        f"Attempting to open serial port {serial_port_name}..."
    )
    ser = None
    async with serial_port_lock:
        try:
            ser = serial.Serial(
                port=serial_port_name,
                baudrate=baud_rate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=SERIAL_TIMEOUT,
            )
            logging.info(
                f"Serial port {serial_port_name} opened for "
                f"{websocket.remote_address}."
            )

            # Create two concurrent tasks for bidirectional communication
            producer_task = asyncio.create_task(
                serial_to_websocket_task(serial_port_name, websocket, ser)
            )
            consumer_task = asyncio.create_task(
                websocket_to_serial_task(serial_port_name, websocket, ser)
            )

            # Wait for both tasks to complete (e.g., if WebSocket disconnects
            # or an error occurs)
            _, pending = await asyncio.wait(
                [producer_task, consumer_task],
                return_when=asyncio.FIRST_COMPLETED,  # Stop if one task completes
            )

            for task in pending:  # Cancel any remaining pending tasks
                task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await task  # Await to ensure cancellation completes

            logging.info(
                f"WebSocket communication closed for {websocket.remote_address}."
            )

        except serial.SerialException as e:
            logging.error(
                f"Failed to open serial port {serial_port_name} for "
                f"{websocket.remote_address}: {e}"
            )
            # Send error to WebSocket client if connection is still open
            try:
                error_message = (
                    f"Error: Could not open serial port {serial_port_name}. {e}".encode(
                        "utf-8"
                    )
                )
                await websocket.send(error_message)
            except Exception:
                pass  # Ignore if WebSocket is already closed
        except Exception as e:
            logging.exception(
                f"An unexpected error occurred in serial_websocket_handler: {e}"
            )
        finally:
            if ser and ser.is_open:
                ser.close()
                logging.info(
                    f"Serial port {serial_port_name} closed for "
                    f"{websocket.remote_address}."
                )


def get_local_ip():
    """Attempts to retrieve the machine's local IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't actually have to be reachable
        # 192.0.2.0/24 is not routable and SonarCloud won't flag a security issue
        s.connect(("192.0.2.255", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"  # Fallback to localhost if no network connection
        logging.warning(
            "Could not determine local IP address, falling back to 127.0.0.1. "
            "The service may not be discoverable on the network."
        )
    finally:
        s.close()
    return IP


async def main():
    """
    Main function to parse arguments, start the WebSocket server, and
    declare the Zeroconf service.
    """
    global zeroconf_instance, service_info

    parser = argparse.ArgumentParser(
        description="WebSocket server to relay data from a serial port "
        "with Zeroconf discovery."
    )
    parser.add_argument(
        "-s",
        "--serial_port",
        type=str,
        default=SERIAL_PORT,
        help="The serial port name to use (e.g., COM1 on Windows, "
        "/dev/ttyUSB0 on Linux).",
    )
    parser.add_argument(
        "-b",
        "--baud_rate",
        type=int,
        default=SERIAL_BAUD_RATE,
        help="The baud rate for the serial port (e.g., 9600, 115200).",
    )
    parser.add_argument(
        "-p",
        "--websocket_port",
        type=int,
        default=WEBSOCKET_PORT,
        help="The WebSocket server port (default: 8080).",
    )
    args = parser.parse_args()
    serial_port_name = args.serial_port
    baud_rate = args.baud_rate
    websocket_port = args.websocket_port
    logging.info(f"Specified serial port: {serial_port_name} at baud rate: {baud_rate}")

    # 1. Start the Zeroconf server and register the service
    zeroconf_instance = AsyncZeroconf()
    local_ip = get_local_ip()
    logging.info(f"Local IP address detected for Zeroconf: {local_ip}")

    # Optional properties for the service (can be useful for clients)
    properties = {
        "api_ver": "0.1",
        "port": str(websocket_port),
        "path": WEBSOCKET_PATH,
        "board_id": (
            f"Ayab Serial to WebSocket Bridge for {serial_port_name} at "
            f"{baud_rate} baud"
        ),
        "serial_port_name": serial_port_name,
        "serial_baud_rate": str(baud_rate),
    }

    service_info = AsyncServiceInfo(
        ZEROCONF_SERVICE_TYPE,
        f"{ZEROCONF_SERVICE_NAME} - {serial_port_name}@{baud_rate}"
        f"._ayab._tcp.local.",  # Full service name including port and baud rate
        addresses=[socket.inet_aton(local_ip)],  # Convert IP to binary format
        port=websocket_port,
        properties=properties,
        server=f"{socket.gethostname()}.local.",  # Hostname of the machine
    )

    logging.info(
        f"Registering Zeroconf service: {ZEROCONF_SERVICE_NAME} for "
        f"{serial_port_name}@{baud_rate} on port {websocket_port}"
    )
    await zeroconf_instance.async_register_service(service_info)

    # 2. Start the WebSocket server
    logging.info(f"Starting WebSocket server on ws://{WEBSOCKET_HOST}:{websocket_port}")
    try:
        # Pass both serial_port_name and baud_rate to the WebSocket handler function
        # using a lambda
        async with websockets.serve(
            lambda ws: serial_websocket_handler(serial_port_name, baud_rate, ws),
            WEBSOCKET_HOST,
            websocket_port,
        ) as server:
            await server.serve_forever()  # Run the server forever
    except Exception as e:
        logging.exception(f"Error starting WebSocket server: {e}")
    finally:
        # Ensure Zeroconf is unregistered and closed upon shutdown
        if zeroconf_instance:
            logging.info("Unregistering Zeroconf service...")
            await zeroconf_instance.async_unregister_all_services()
            logging.info("Closing Zeroconf instance...")
            await zeroconf_instance.async_close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Server stopped by user.")
    except Exception as e:
        logging.exception(f"Fatal error: {e}")
