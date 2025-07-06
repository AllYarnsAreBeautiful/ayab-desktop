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

from __future__ import annotations
from PySide6.QtCore import QOperatingSystemVersion
from PySide6.QtWidgets import QMenuBar

from .menu_gui import Ui_MenuBar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ayab import GuiMain


class Menu(QMenuBar):
    """
    Menu bar object and associated methods.

    @author Tom Price
    @date   July 2020
    """

    def __init__(self, parent: GuiMain):
        super().__init__(parent)

        # Use native menubar on macOS, not elsewhere (i.e. Linux)
        if (
            QOperatingSystemVersion.currentType()
            != QOperatingSystemVersion.OSType.MacOS
        ):
            self.setNativeMenuBar(False)

        self.ui = Ui_MenuBar()
        self.ui.setupUi(self)
        self.setup()

    def setup(self) -> None:
        self.addAction(self.ui.menu_tools.menuAction())
        self.addAction(self.ui.menu_preferences.menuAction())
        self.addAction(self.ui.menu_help.menuAction())

    def depopulate(self) -> None:
        try:
            self.removeAction(self.ui.menu_image_actions.menuAction())
        except Exception:
            pass
        self.removeAction(self.ui.menu_tools.menuAction())
        self.removeAction(self.ui.menu_preferences.menuAction())
        self.removeAction(self.ui.menu_help.menuAction())

    def repopulate(self) -> None:
        self.addAction(self.ui.menu_image_actions.menuAction())
        self.setup()

    def add_image_actions(self) -> None:
        # This workaround is necessary because
        # self.menu_image_actions.menuAction().setEnabled(True)
        # does not seems to work (at least, not on Ubuntu 16.04)
        # Tom Price June 2020
        self.depopulate()
        self.repopulate()
