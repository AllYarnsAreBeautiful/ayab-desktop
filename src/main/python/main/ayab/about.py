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
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt, QCoreApplication

from .about_gui import Ui_AboutForm
from . import utils
from . import ayab_logo_rc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ayab import GuiMain


class About(QFrame):
    ayab_logo_rc

    def __init__(self, parent: GuiMain):
        super().__init__()
        self.__ui = Ui_AboutForm()
        self.__ui.setupUi(self)
        self.__ui.title_label.setText(
            f"AYAB {utils.package_version(parent.app_context)}"
        )
        self.__ui.link_label.setText(
            QCoreApplication.translate("MainWindow", "Website")
            + ": <a href='https://ayab-knitting.com'>https://ayab-knitting.com</a>"
        )
        self.__ui.link_label.setTextFormat(Qt.TextFormat.RichText)
        self.__ui.link_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction
        )
        self.__ui.link_label.setOpenExternalLinks(True)
        self.__ui.manual_label.setText(
            QCoreApplication.translate("MainWindow", "Manual")
            + ": <a href='https://manual.ayab-knitting.com'>"
            + "https://manual.ayab-knitting.com</a>"
        )
        self.__ui.manual_label.setTextFormat(Qt.TextFormat.RichText)
        self.__ui.manual_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction
        )
        self.__ui.manual_label.setOpenExternalLinks(True)
