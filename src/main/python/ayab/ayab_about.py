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

from .ayab_about_gui import Ui_AboutForm
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QCoreApplication


class About(object):
    def __init__(self, app_context):
        self.__version = "package_version"
        filename_version = app_context.get_resource("ayab/package_version")
        with open(filename_version) as version_file:
            self.__version = version_file.read().strip()

    def show(self):
        self.__about = QFrame()
        __about_ui = Ui_AboutForm()
        __about_ui.setupUi(self.__about)
        __about_ui.title_label.setText(
            QCoreApplication.translate("MainWindow", "All Yarns Are Beautiful")
            + " v " + self.__version)
        __about_ui.link_label.setText(
            QCoreApplication.translate("MainWindow", "Website") +
            ": <a href='http://ayab-knitting.com'>http://ayab-knitting.com</a>"
        )
        __about_ui.link_label.setTextFormat(Qt.RichText)
        __about_ui.link_label.setTextInteractionFlags(
            Qt.TextBrowserInteraction)
        __about_ui.link_label.setOpenExternalLinks(True)
        __about_ui.manual_label.setText(
            QCoreApplication.translate("MainWindow", "Manual") +
            ": <a href='http://manual.ayab-knitting.com'>http://manual.ayab-knitting.com</a>"
        )
        __about_ui.manual_label.setTextFormat(Qt.RichText)
        __about_ui.manual_label.setTextInteractionFlags(
            Qt.TextBrowserInteraction)
        __about_ui.manual_label.setOpenExternalLinks(True)
        self.__about.show()
