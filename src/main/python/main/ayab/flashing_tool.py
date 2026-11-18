# -*- coding: utf-8 -*-
# This file is part of AYAB.
#
#    AYAB is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AYAB is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with AYAB.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright 2014 Sebastian Oliva, Christian Obersteiner,
#       Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

"""Flashing tools for various microcontroller types."""

from __future__ import annotations
from abc import ABC, abstractmethod
from subprocess import check_output, CalledProcessError, STDOUT
from typing import TYPE_CHECKING, Optional, Any
import logging
import os
import platform
import shutil
import time

import serial

if TYPE_CHECKING:
    from typing import Protocol

    class AppContext(Protocol):
        def get_resource(self, path: str) -> str: ...

else:
    AppContext = Any


class FlashingError(Exception):
    """Raised when flashing a firmware fails."""


class FlashingTool(ABC):
    """Abstract base class for flashing tools running an external executable.

    The executables are bundled in `ayab/firmware/` as `<name>.exe` (Windows),
    `<name>_mac` (macOS) and `<name>_linux` (Linux x86_64). On other Linux
    architectures, the executable is looked up in PATH.
    """

    # Base name of the executable
    name: str
    # Timeout of the flashing command, in seconds
    timeout: float = 10

    def __init__(self) -> None:
        self._logger = logging.getLogger(type(self).__name__)

    @abstractmethod
    def generate_command(
        self,
        os_name: str,
        port: str,
        firmware_path: str,
        app_context: AppContext,
    ) -> Optional[str]:
        """Build the flashing command line, or None if it cannot be run."""

    @abstractmethod
    def get_display_name(self) -> str:
        """Get user-friendly name of the tool."""

    def flash(
        self,
        os_name: str,
        port: str,
        firmware_path: str,
        app_context: AppContext,
    ) -> None:
        """Flash the firmware to the controller connected to the port.

        Args:
            os_name: The operating system name ('Windows', 'Linux', 'Darwin')
            port: The serial port to flash to
            firmware_path: Full path to the firmware file
            app_context: The application context for resource access

        Raises:
            FlashingError: if flashing failed (details are logged)
        """
        command = self.generate_command(os_name, port, firmware_path, app_context)
        if command is None:
            raise FlashingError(f"{self.name} not found or invalid firmware file")
        self._run(command)

    def _run(self, command: str) -> None:
        self._logger.debug("Running: %s", command)
        try:
            output = check_output(
                command, stderr=STDOUT, timeout=self.timeout, shell=True
            )
        except CalledProcessError as e:
            self._logger.error("%s output: %r", self.name, e.output)
            raise FlashingError(f"{self.name} failed: {e}") from e
        except Exception as e:
            raise FlashingError(f"{self.name} failed: {e!r}") from e
        self._logger.debug("%s output: %r", self.name, output)

    def verify_firmware_path(self, firmware_path: str) -> bool:
        """Verify that the firmware file exists and is valid."""
        if not os.path.exists(firmware_path) or os.path.getsize(firmware_path) <= 0:
            return False
        return True

    @staticmethod
    def is_bundled(os_name: str) -> bool:
        """Whether a bundled executable is used on this machine."""
        if os_name == "Linux":
            return platform.machine() in ("x86_64", "AMD64")
        return os_name in ("Windows", "Darwin")

    def _get_tool_path(self, os_name: str, app_context: AppContext) -> Optional[str]:
        """Get the quoted path to the executable, or None if not found."""
        suffixes = {"Windows": ".exe", "Darwin": "_mac", "Linux": "_linux"}
        if self.is_bundled(os_name):
            path = app_context.get_resource(
                f"ayab/firmware/{self.name}{suffixes[os_name]}"
            )
        elif os_name == "Linux":
            # No bundled executable for this architecture: look in PATH
            found = shutil.which(self.name)
            if found is None:
                return None
            path = found
        else:
            return None
        return '"' + path + '"'


class AvrDudeTool(FlashingTool):
    """Flashing tool for AVR microcontrollers (Arduino Uno, etc.)."""

    name = "avrdude"

    def __init__(self, device: str, programmer: str):
        """Initialize AVRDUDE tool.

        Args:
            device: The AVR device name (e.g., 'atmega328p')
            programmer: The programmer type (e.g., 'arduino')
        """
        super().__init__()
        self.device = device
        self.programmer = programmer

    def generate_command(
        self,
        os_name: str,
        port: str,
        firmware_path: str,
        app_context: AppContext,
    ) -> Optional[str]:
        tool_path = self._get_tool_path(os_name, app_context)
        if not tool_path:
            return None

        if not self.verify_firmware_path(firmware_path):
            return None

        exec_command = (
            f"{tool_path} -p {self.device} -c {self.programmer} -P {port} -b115200"
            + f' -D -Uflash:w:"{firmware_path}":i '
        )

        # The bundled binaries (all the same avrdude version) share one config
        # file; a system avrdude found in PATH uses its own.
        if self.is_bundled(os_name):
            conf_path = app_context.get_resource("ayab/firmware/avrdude.conf")
            exec_command += f' -C "{conf_path}"'

        return exec_command

    def get_display_name(self) -> str:
        return "AVRDUDE"


class BossacTool(FlashingTool):
    """Flashing tool for the Renesas RA4M1 of the Arduino UNO R4 WiFi.

    Same procedure as the Arduino IDE (ArduinoCore-renesas, `unor4wifi`): a
    "1200 bps touch" on the serial port makes the ESP32-S3 USB bridge reset
    the RA4M1 into its bootloader, then bossac (Arduino fork) writes the
    `.bin` firmware through the bridge. The port does not change.
    """

    name = "bossac"
    timeout = 60

    def __init__(self, bootloader_delay: float = 1.0):
        """Initialize BOSSAC tool.

        Args:
            bootloader_delay: Seconds to wait after the 1200 bps touch for
                the bootloader to start
        """
        super().__init__()
        self.bootloader_delay = bootloader_delay

    def generate_command(
        self,
        os_name: str,
        port: str,
        firmware_path: str,
        app_context: AppContext,
    ) -> Optional[str]:
        tool_path = self._get_tool_path(os_name, app_context)
        if not tool_path:
            return None

        if not self.verify_firmware_path(firmware_path):
            return None

        return f'{tool_path} --port="{port}" -U -e -w "{firmware_path}" -R'

    def flash(
        self,
        os_name: str,
        port: str,
        firmware_path: str,
        app_context: AppContext,
    ) -> None:
        command = self.generate_command(os_name, port, firmware_path, app_context)
        if command is None:
            raise FlashingError("bossac not found or invalid firmware file")
        self.touch_1200bps(port)
        time.sleep(self.bootloader_delay)
        self._run(command)

    def touch_1200bps(self, port: str) -> None:
        """Open and close the port at 1200 bps to enter the bootloader."""
        self._logger.debug("1200 bps touch on %s", port)
        try:
            with serial.Serial(port, 1200) as s:
                s.dtr = False
        except serial.SerialException as e:
            raise FlashingError(f"1200 bps touch on {port} failed: {e}") from e

    def get_display_name(self) -> str:
        return "BOSSAC"


class FlashingToolFactory:
    """Factory for creating flashing tool instances based on controller type."""

    @staticmethod
    def create_tool(controller_type: str) -> Optional[FlashingTool]:
        """Create a flashing tool for the given controller type.

        Args:
            controller_type: The controller identifier (e.g., 'uno', 'r4_wifi')

        Returns:
            A FlashingTool instance, or None if controller type is unknown
        """
        controllers = {
            "uno": AvrDudeTool(device="atmega328p", programmer="arduino"),
            "r4_wifi": BossacTool(),
        }
        return controllers.get(controller_type)
