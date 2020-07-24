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
#    Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop
"""Functions that do not have a parent class."""

import logging
import numpy as np
import serial.tools.list_ports
import requests

from PyQt5.QtWidgets import QMessageBox


def even(x):
    return x % 2 == 0


def odd(x):
    return x % 2 == 1


def display_blocking_popup(message="", message_type="info"):
    """Display a modal message box."""
    logging.debug("MessageBox {}: '{}'".format(message_type, message))
    box_function = {
        "error": QMessageBox.critical,
        "info": QMessageBox.information,
        "question": QMessageBox.question,
        "warning": QMessageBox.warning
    }
    message_box_function = box_function.get(message_type)
    ret = message_box_function(None, "AYAB", message, QMessageBox.Ok,
                               QMessageBox.Ok)
    if ret == QMessageBox.Ok:
        return True


# USB port functions


def populate_ports(combo_box=None, port_list=None):
    """Populate combo box with a list of ports."""
    if not port_list:
        port_list = get_serial_ports()
    combo_box.clear()
    for item in port_list:
        # TODO: should display the info of the device.
        combo_box.addItem(item[0])


def get_serial_ports():
    """Return a list of all USB serial ports."""
    return list(serial.tools.list_ports.grep("USB"))


# Color functions


def rgb2array(color):
    return np.array([color // 0x1000, (color // 0x100) & 0xFF, color & 0xFF])


def greyscale(rgb):
    return np.dot([.299, .587, .114], rgb)


def contrast_color(color):
    return [0x000000, 0xFFFFFF][greyscale(rgb2array(color)) < 0x80]


# Version


def package_version(app_context):
    version = "package_version"
    filename_version = app_context.get_resource("ayab/package_version")
    with open(filename_version) as version_file:
        version = version_file.read().strip()
    return version

def latest_version(repo):
    r = requests.get("https://api.github.com/repos/" + repo + "/releases/latest")
    obj = r.json()
    if obj["draft"] == False and obj["prerelease"] == False:
        return obj["tag_name"]
