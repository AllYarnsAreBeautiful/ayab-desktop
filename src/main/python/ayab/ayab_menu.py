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
"""Provides an Interface for users to operate AYAB using a GUI."""

from PyQt5.QtWidgets import QMenuBar
from .ayab_menu_gui import Ui_MenuBar


class Menu(QMenuBar):
    def __init__(self, parent):
        super(QMenuBar, self).__init__(parent)
        self.ui = Ui_MenuBar()
        self.ui.setupUi(self)

    def setup(self):
        self.addAction(self.ui.menu_tools.menuAction())
        self.addAction(self.ui.menu_preferences.menuAction())
        self.addAction(self.ui.menu_help.menuAction())

    def depopulate(self):
        try:
            self.removeAction(self.menu_image_actions.menuAction())
        except Exception:
            pass
        self.removeAction(self.ui.menu_tools.menuAction())

    def repopulate(self):
        self.removeAction(self.ui.menu_preferences.menuAction())
        self.removeAction(self.ui.menu_help.menuAction())
        self.addAction(self.ui.menu_image_actions.menuAction())
        self.setup()

    def add_image_actions(self):
        # This workaround is necessary because
        # self.__actionImageActions.setEnabled(True)
        # does not seems to work (at least, not on Ubuntu 16.04)
        # Tom Price June 2020
        self.depopulate()
        self.repopulate()
