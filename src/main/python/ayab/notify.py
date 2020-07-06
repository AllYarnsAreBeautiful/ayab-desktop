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

import logging
from PyQt5.QtWidgets import QMessageBox


def display_blocking_popup(message="", message_type="info"):
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
