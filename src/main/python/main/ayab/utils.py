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
#    Copyright 2013-2020 Sebastian Oliva, Christian Obersteiner,
#       Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop
"""Functions that do not have a parent class."""

from __future__ import annotations
import logging
from typing import Any, Callable, Literal, Optional, TypeAlias, cast
import numpy as np
import numpy.typing as npt
import serial.tools.list_ports

from PySide6.QtWidgets import QMessageBox, QComboBox


def even(x: int) -> bool:
    return x % 2 == 0


def odd(x: int) -> bool:
    return x % 2 == 1


MessageTypes: TypeAlias = Literal["error", "info", "question", "warning"]
QMessageBoxFunc: TypeAlias = Callable[..., QMessageBox.StandardButton]


def display_blocking_popup(
    message: str = "", message_type: MessageTypes = "info"
) -> bool:
    """Display a modal message box."""
    logging.debug(f"MessageBox {message_type}: '{message}'")
    box_function: dict[MessageTypes, QMessageBoxFunc] = {
        "error": QMessageBox.critical,
        "info": QMessageBox.information,
        "question": QMessageBox.question,
        "warning": QMessageBox.warning,
    }
    message_box_function = box_function[message_type]
    ret = message_box_function(
        None,
        "AYAB",
        message,
        QMessageBox.StandardButton.Ok,
        QMessageBox.StandardButton.Ok,
    )
    if ret == QMessageBox.StandardButton.Ok:
        return True
    return False


# USB port functions


def populate_ports(
    combo_box: Optional[QComboBox] = None, port_list: Optional[list[str]] = None
) -> None:
    """Populate combo box with a list of ports."""
    if not combo_box:
        return
    if not port_list:
        port_list = get_serial_ports()
    combo_box.clear()
    for item in port_list:
        # TODO: should display the info of the device.
        combo_box.addItem(item[0])


def get_serial_ports() -> list[str]:
    """Return a list of all USB serial ports."""
    return list(serial.tools.list_ports.grep("USB"))  # type: ignore


# Color functions


def rgb2array(color: int) -> npt.NDArray[np.int_]:
    return np.array([color // 0x1000, (color // 0x100) & 0xFF, color & 0xFF])


def greyscale(rgb: npt.NDArray[np.int_]) -> int:
    return cast(int, np.dot([0.299, 0.587, 0.114], rgb))


def contrast_color(color: int) -> int:
    return [0x000000, 0xFFFFFF][greyscale(rgb2array(color)) < 0x80]


# Version


def package_version(app_context: Any) -> str:
    try:
        filename_version = app_context.get_resource("ayab/package_version")
        with open(filename_version) as version_file:
            return version_file.read().strip()
    except FileNotFoundError:
        # Return a fake version number for local development,
        # to disable update checking
        return "999.99.9"
