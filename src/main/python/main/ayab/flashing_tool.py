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
from typing import TYPE_CHECKING, Optional, Any
from subprocess import run, PIPE
import re
import os

if TYPE_CHECKING:
    from typing import Protocol

    class AppContext(Protocol):
        def get_resource(self, path: str) -> str: ...

else:
    AppContext = Any


class FlashingTool(ABC):
    """Abstract base class for all flashing tools (avrdude, esptool, bossac, etc.)."""

    @abstractmethod
    def generate_command(
        self,
        os_name: str,
        port: str,
        firmware_path: str,
        app_context: AppContext,
    ) -> Optional[str]:
        """Generate the flashing command for this tool.

        Args:
            os_name: The operating system name ('Windows', 'Linux', 'Darwin')
            port: The serial port to flash to
            firmware_path: Full path to the firmware file
            app_context: The application context for resource access

        Returns:
            The complete command string to execute, or None if error
        """
        pass

    @abstractmethod
    def get_display_name(self) -> str:
        """Get user-friendly name of the tool."""
        pass

    def verify_firmware_path(self, firmware_path: str) -> bool:
        """Verify that the firmware file exists and is valid."""
        if not os.path.exists(firmware_path) or os.path.getsize(firmware_path) <= 0:
            return False
        return True

    def get_tool_path(self, os_name: str, app_context: AppContext) -> Optional[str]:
        """Get the path to the tool executable.

        This base implementation tries to find the tool from app resources.
        Child classes should override this for tool-specific paths.
        """
        return None


class AvrDudeTool(FlashingTool):
    """Flashing tool for AVR microcontrollers (Arduino Uno, etc.)."""

    def __init__(self, device: str, programmer: str):
        """Initialize AVRDUDE tool.

        Args:
            device: The AVR device name (e.g., 'atmega328p')
            programmer: The programmer type (e.g., 'arduino')
        """
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

        # Build avrdude command
        exec_command = (
            f"{tool_path} -p {self.device} -c {self.programmer} -P {port} -b115200"
            + f' -D -Uflash:w:"{firmware_path}":i '
        )

        # Add config file if needed
        if os_name == "Windows":
            conf_path = app_context.get_resource("ayab/firmware/avrdude.conf")
            exec_command += f' -C "{conf_path}"'
        elif os_name == "Darwin":
            conf_path = app_context.get_resource("ayab/firmware/avrdude_mac.conf")
            exec_command += f' -C "{conf_path}"'

        return exec_command

    def get_display_name(self) -> str:
        return "AVRDUDE"

    def _get_tool_path(self, os_name: str, app_context: AppContext) -> Optional[str]:
        """Get the path to avrdude executable."""
        if os_name == "Windows":
            path = app_context.get_resource("ayab/firmware/avrdude.exe")
            return '"' + path + '"'
        elif os_name == "Darwin":
            path = app_context.get_resource("ayab/firmware/avrdude_mac")
            return '"' + path + '"'
        elif os_name == "Linux":
            # Try to find avrdude in PATH
            try:
                result = run(["which", "avrdude"], stdout=PIPE, stderr=PIPE)
                path = re.sub(r"\n$", r"", result.stdout.decode("ascii"))
                return path
            except Exception:
                return None
        return None


class EspTool(FlashingTool):
    """Flashing tool for ESP32-based microcontrollers (Arduino R4 WiFi, etc.)."""

    def __init__(self, chip: str = "esp32s3", baud: int = 460800):
        """Initialize ESPTOOL.

        Args:
            chip: The ESP32 chip type (e.g., 'esp32s3')
            baud: The baud rate for flashing
        """
        self.chip = chip
        self.baud = baud

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

        cmd = (
            f"{tool_path} --chip {self.chip} --port {port} --baud {self.baud} "
            "--before default_reset --after hard_reset "
            f'write_flash 0x0 "{firmware_path}"'
        )
        return cmd

    def get_display_name(self) -> str:
        return "ESPTOOL"

    def _get_tool_path(self, os_name: str, app_context: AppContext) -> Optional[str]:
        """Get the path to esptool executable."""
        if os_name == "Windows":
            path = app_context.get_resource("ayab/firmware/esptool.exe")
            return '"' + path + '"'
        elif os_name == "Darwin":
            path = app_context.get_resource("ayab/firmware/esptool_mac")
            return '"' + path + '"'
        elif os_name == "Linux":
            # Try to find esptool in PATH (usually esptool.py)
            for tool in ["esptool.py", "esptool"]:
                try:
                    result = run(["which", tool], stdout=PIPE, stderr=PIPE)
                    path = re.sub(r"\n$", r"", result.stdout.decode("ascii"))
                    if path:
                        return path
                except Exception:
                    continue
            return None
        return None


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
            "r4_wifi": EspTool(chip="esp32s3", baud=460800),
        }
        return controllers.get(controller_type)
