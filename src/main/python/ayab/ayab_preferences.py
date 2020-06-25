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
"""
Module providing abstraction layer for user preferences.

User preferences are configured on startup.
The method of configuration may differ depending on the OS.
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSettings, Qt
from .ayab_prefs_gui import Ui_PrefsDialog


def str2bool(qvariant):
    if type(qvariant) == str:
        return qvariant.lower() == "true"
    else:
        return qvariant


class Preferences:
            
    def __init__(self):
        QtCore.QCoreApplication.setOrganizationName("AYAB")
        QtCore.QCoreApplication.setOrganizationDomain("ayab-knitting.com")
        QtCore.QCoreApplication.setApplicationName("ayab")
        self.settings = QSettings()
        self.settings.setFallbacksEnabled(False)
        if self.settings.allKeys() == []:
            self.reset()
        else:
            self.settings.setValue("automatic_mirroring",
                                   str2bool(self.settings.value("automatic_mirroring")))
            self.settings.setValue("default_infinite_repeat",
                                   str2bool(self.settings.value("default_infinite_repeat")))
            self.settings.setValue("quiet_mode",
                                   str2bool(self.settings.value("quiet_mode")))

    def reset(self):
        '''Reset preferences to default values'''
        self.settings.setValue("automatic_mirroring", False)
        self.settings.setValue("default_knitting_mode", "Singlebed")
        self.settings.setValue("default_infinite_repeat", False)
        self.settings.setValue("default_alignment", "center")
        self.settings.setValue("quiet_mode", False)

    def setPrefsDialog(self):
        return PrefsDialog(self).exec_()


class PrefsDialog(QtWidgets.QDialog):
    '''GUI to set preferences'''

    def __init__(self, parent):
        super(PrefsDialog, self).__init__(None)
        self.__reset = parent.reset
        self.__settings = parent.settings
        self.__ui = Ui_PrefsDialog()
        self.__ui.setupUi(self)
        self.__ui.default_knitting_mode_box.currentIndexChanged.connect(self.__update_default_knitting_mode_setting)
        self.__ui.default_infinite_repeat_checkbox.toggled.connect(self.__toggle_default_infinite_repeat_setting)
        self.__ui.default_alignment_box.currentIndexChanged.connect(self.__update_default_alignment_setting)
        self.__ui.automatic_mirroring_checkbox.toggled.connect(self.__toggle_automatic_mirroring_setting)
        self.__ui.quiet_mode_checkbox.toggled.connect(self.__toggle_quiet_mode_setting)
        self.__ui.reset.clicked.connect(self.__reset_and_refresh)
        self.__ui.enter.clicked.connect(self.accept)
        self.__refresh()

    def __update_default_knitting_mode_setting(self):
        self.__settings.setValue("default_knitting_mode",
                               self.__ui.default_knitting_mode_box.itemText(self.__ui.default_knitting_mode_box.currentIndex()))
        return

    def __toggle_default_infinite_repeat_setting(self):
        if self.__ui.default_infinite_repeat_checkbox.isChecked():
            self.__settings.setValue("default_infinite_repeat", True)
        else:
            self.__settings.setValue("default_infinite_repeat", False)
        return

    def __update_default_alignment_setting(self):
        self.__settings.setValue("default_alignment",
                               self.__ui.default_alignment_box.itemText(self.__ui.default_alignment_box.currentIndex()))
        return

    def __toggle_automatic_mirroring_setting(self):
        if self.__ui.automatic_mirroring_checkbox.isChecked():
            self.__settings.setValue("automatic_mirroring", True)
        else:
            self.__settings.setValue("automatic_mirroring", False)
        return

    def __toggle_quiet_mode_setting(self):
        if self.__ui.quiet_mode_checkbox.isChecked():
            self.__settings.setValue("quiet_mode", True)
        else:
            self.__settings.setValue("quiet_mode", False)
        return

    def __refresh(self):
        '''Update preferences GUI to current values'''
        self.__ui.default_knitting_mode_box.setCurrentIndex(
            self.__ui.default_knitting_mode_box.findText(
                self.__settings.value("default_knitting_mode")))
        if str2bool(self.__settings.value("default_infinite_repeat")):
            self.__ui.default_infinite_repeat_checkbox.setCheckState(Qt.Checked)
        else:
            self.__ui.default_infinite_repeat_checkbox.setCheckState(Qt.Unchecked)
        self.__ui.default_alignment_box.setCurrentIndex(
            self.__ui.default_alignment_box.findText(
                self.__settings.value("default_alignment")))
        if str2bool(self.__settings.value("automatic_mirroring")):
            self.__ui.automatic_mirroring_checkbox.setCheckState(Qt.Checked)
        else:
            self.__ui.automatic_mirroring_checkbox.setCheckState(Qt.Unchecked)
        if str2bool(self.__settings.value("quiet_mode")):
            self.__ui.quiet_mode_checkbox.setCheckState(Qt.Checked)
        else:
            self.__ui.quiet_mode_checkbox.setCheckState(Qt.Unchecked)

    def __reset_and_refresh(self):
        self.__reset()
        self.__refresh()
        return

