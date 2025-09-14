import contextlib
import websockets.exceptions
import websockets.protocol
import websockets.sync.client
import threading


"""Handles the serial communication protocol over a websocket.

This modules exposes an interface compatible with the Serial class
for websocket communication.
"""


class WebsocketSerial:
    def __init__(self, uri: str, timeout: float | None):
        try:
            self._ws = websockets.sync.client.connect(uri)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to websocket {uri}: {e}") from e
        self._timeout = timeout
        self._rxbuffer = b""
        self._lock = threading.Lock()

    @property
    def is_open(self) -> bool:
        return self._ws.state == websockets.protocol.State.OPEN

    @property
    def in_waiting(self) -> int:
        with self._lock:
            return len(self._rxbuffer)

    def read(self, size: int = 1) -> bytes:
        with self._lock:
            while size > len(self._rxbuffer):
                try:
                    data = self._ws.recv(self._timeout)
                    if isinstance(data, bytes):
                        self._rxbuffer += data
                except (TimeoutError, websockets.exceptions.ConnectionClosed):
                    break

            data = self._rxbuffer[0:size]
            self._rxbuffer = self._rxbuffer[size:]
        return data

    def write(self, data: bytes) -> int:
        try:
            with self._lock:
                self._ws.send(data)
                return len(data)
        except websockets.exceptions.ConnectionClosed:
            raise ConnectionError("WebSocket connection is closed") from None

    def close(self) -> None:
        with self._lock:
            with contextlib.suppress(Exception):
                self._ws.close()

    def flush(self) -> None:
        """Flush write buffers, if applicable."""
        pass  # WebSockets handle this automatically

    def reset_input_buffer(self) -> None:
        """Clear input buffer."""
        with self._lock:
            self._rxbuffer = b""

    def reset_output_buffer(self) -> None:
        """Clear output buffer."""
        pass  # WebSockets handle this automatically
