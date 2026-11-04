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
from PySide6.QtGui import QAction

from .menu_gui import Ui_MenuBar
from typing import TYPE_CHECKING, cast

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
        self.__parent = parent
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
        """Initial menu setup"""
        self.addAction(self.ui.menu_tools.menuAction())
        self.addAction(self.ui.menu_preferences.menuAction())
        self.addAction(self.ui.menu_help.menuAction())

        # Wire recent file actions once (guard prevents re-wiring on repopulate())
        if not hasattr(self, "recents"):
            self.recents = [
                getattr(self.ui, "action_recent_" + str(x))
                for x in range(self.__parent.prefs.MAX_RECENT_COUNT)
            ]
            for action in self.recents:
                action.triggered.connect(self.loadRecent)

        # Set up recent files menus
        self.showRecents()

    # Show recent files menus
    def showRecents(self) -> None:
        """Update recent files menu"""

        # Set recents invisible
        for action in self.recents:
            action.setVisible(False)

        # Set recents menu invisible as well
        self.ui.menu_recent_files.menuAction().setVisible(False)

        # Get file names from recents list
        # and make items visible if there are files available.
        i = 0
        while i < self.__parent.prefs.MAX_RECENT_COUNT and i < len(self.__parent.prefs.recentFiles):
            self.recents[i].setText(self.__parent.prefs.recentFiles[i])
            self.recents[i].setVisible(True)
            i += 1

        # Set visible toplevel menu item if there are recent files available
        if i > 0:
            self.ui.menu_recent_files.menuAction().setVisible(True)

    # Function is a recent menu click handler
    # Load image from file
    def loadRecent(self, _: QAction) -> None:
        """Recent menu action click handler"""
        filename = cast(QAction, self.sender()).text()
        self.__parent.scene.ayabimage.load(filename)

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
