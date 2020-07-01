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

from os import path
from glob import glob
from PyQt5.QtCore import Qt, QSettings, QLocale
from PyQt5.QtWidgets import QDialog
from .ayab_prefs_gui import Ui_PrefsDialog
from .plugins.ayab_plugin.ayab_options import KnittingMode, Alignment


def str2bool(qvariant):
    if type(qvariant) == str:
        return qvariant.lower() == "true"
    else:
        return qvariant


class Preferences:
            
    def __init__(self, app_context):
        self.__app_context = app_context
        self.settings = QSettings()
        self.settings.setFallbacksEnabled(False)
        if self.settings.allKeys() == []:
            self.reset()
        else:
            self.settings.setValue("automatic_mirroring",
                                   str2bool(self.settings.value("automatic_mirroring")))
            self.settings.setValue("default_knitting_mode",
                                   int(self.settings.value("default_knitting_mode")))
            self.settings.setValue("default_infinite_repeat",
                                   str2bool(self.settings.value("default_infinite_repeat")))
            self.settings.setValue("default_alignment",
                                   int(self.settings.value("default_alignment")))
            self.settings.setValue("quiet_mode",
                                   str2bool(self.settings.value("quiet_mode")))

    def reset(self):
        '''Reset preferences to default values'''
        self.settings.setValue("automatic_mirroring", False)
        self.settings.setValue("default_knitting_mode", "0")
        self.settings.setValue("default_infinite_repeat", False)
        self.settings.setValue("default_alignment", "0")
        self.settings.setValue("quiet_mode", False)
        default = self.default_locale()
        available = self.available_locales()
        if default in available:
            self.settings.setValue("language", default)
        else:
            self.settings.setValue("language", "en_US")

    def set_prefs_dialog(self):
        return PrefsDialog(self).exec_()

    def default_locale(self):
        return QLocale.system().name()

    def available_locales(self):
        lang_dir = self.__app_context.get_resource("ayab/translations")
        lang_files = glob(path.join(lang_dir, "ayab_trans.*.ts"))
        return sorted(map(self.__locale, lang_files))

    def language(self, loc):
        lang = loc[0:3]
        country = loc[3:6]
        # return QLocale.languageToScript(QLocale(lang).language()) \
        return QLocale(loc).nativeLanguageName()  # + " (" + country + ")"

    def __locale(self, string):
        i = string.rindex("_")
        return string[i-2:i+3]


class PrefsDialog (QDialog):
    '''GUI to set preferences'''

    def __init__(self, parent):
        super(PrefsDialog, self).__init__(None)
        self.__reset = parent.reset
        self.__settings = parent.settings

        # set up preferences dialog
        self.__ui = Ui_PrefsDialog()
        self.__ui.setupUi(self)

        # add combo box items
        KnittingMode.addItems(self.__ui.default_knitting_mode_box)
        Alignment.addItems(self.__ui.default_alignment_box)
        for loc in parent.available_locales():
            self.__ui.language_box.addItem(parent.language(loc), loc)

        # connect dialog box buttons
        self.__ui.default_knitting_mode_box.currentIndexChanged.connect(self.__update_default_knitting_mode_setting)
        self.__ui.default_infinite_repeat_checkbox.toggled.connect(self.__toggle_default_infinite_repeat_setting)
        self.__ui.default_alignment_box.currentIndexChanged.connect(self.__update_default_alignment_setting)
        self.__ui.automatic_mirroring_checkbox.toggled.connect(self.__toggle_automatic_mirroring_setting)
        self.__ui.quiet_mode_checkbox.toggled.connect(self.__toggle_quiet_mode_setting)
        self.__ui.language_box.currentIndexChanged.connect(self.__update_language_setting)
        self.__ui.reset.clicked.connect(self.__reset_and_refresh)
        self.__ui.enter.clicked.connect(self.accept)

        # update buttons from settings
        self.__refresh()

    def __update_default_knitting_mode_setting(self):
        self.__settings.setValue("default_knitting_mode",
            self.__ui.default_knitting_mode_box.currentIndex())

    def __toggle_default_infinite_repeat_setting(self):
        if self.__ui.default_infinite_repeat_checkbox.isChecked():
            self.__settings.setValue("default_infinite_repeat", True)
        else:
            self.__settings.setValue("default_infinite_repeat", False)

    def __update_default_alignment_setting(self):
        self.__settings.setValue("default_alignment",
            self.__ui.default_alignment_box.currentIndex())

    def __toggle_automatic_mirroring_setting(self):
        if self.__ui.automatic_mirroring_checkbox.isChecked():
            self.__settings.setValue("automatic_mirroring", True)
        else:
            self.__settings.setValue("automatic_mirroring", False)

    def __toggle_quiet_mode_setting(self):
        if self.__ui.quiet_mode_checkbox.isChecked():
            self.__settings.setValue("quiet_mode", True)
        else:
            self.__settings.setValue("quiet_mode", False)

    def __update_language_setting(self):
        self.__settings.setValue("language",
            self.__ui.language_box.currentData())

    def __refresh(self):
        '''Update preferences GUI to current values'''
        self.__ui.default_knitting_mode_box.setCurrentIndex(
            int(self.__settings.value("default_knitting_mode")))
        if str2bool(self.__settings.value("default_infinite_repeat")):
            self.__ui.default_infinite_repeat_checkbox.setCheckState(Qt.Checked)
        else:
            self.__ui.default_infinite_repeat_checkbox.setCheckState(Qt.Unchecked)
        self.__ui.default_alignment_box.setCurrentIndex(
            int(self.__settings.value("default_alignment")))
        if str2bool(self.__settings.value("automatic_mirroring")):
            self.__ui.automatic_mirroring_checkbox.setCheckState(Qt.Checked)
        else:
            self.__ui.automatic_mirroring_checkbox.setCheckState(Qt.Unchecked)
        if str2bool(self.__settings.value("quiet_mode")):
            self.__ui.quiet_mode_checkbox.setCheckState(Qt.Checked)
        else:
            self.__ui.quiet_mode_checkbox.setCheckState(Qt.Unchecked)
        self.__ui.language_box.setCurrentIndex(
            self.__ui.language_box.findData(
                self.__settings.value("language")))

    def __reset_and_refresh(self):
        self.__reset()
        self.__refresh()

