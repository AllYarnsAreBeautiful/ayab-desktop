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
#    Copyright 2014 Sebastian Oliva, Christian Obersteiner, Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop
"""Notification methods using the status bar."""

from __future__ import annotations
import logging
from PySide6.QtWidgets import QStatusBar
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ayab import GuiMain


class StatusBar(QStatusBar):
    def __init__(self, parent:GuiMain):
        super().__init__(parent)

    def update(self, text:str, log:bool=True)->None: #type: ignore
        """Update the message in the status bar."""
        if log:
            logging.info("Status bar: " + text)
        self.showMessage(text)
