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

import re

from PyQt5.QtCore import Qt, QSettings, QCoreApplication
from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QCheckBox, QComboBox

from .prefs_gui import Ui_Prefs
from .observable import Observable
from .engine.options import Alignment
from .engine.mode import Mode
from .machine import Machine
from .language import Language


def str2bool(qvariant):
    if type(qvariant) == str:
        return qvariant.lower() == "true"
    else:
        return qvariant


class Preferences(Observable):
    """Default settings class.

    Variable names and classes are defined in the dict `variables`.
    Classes other than `bool` are expected to have a method `add_items`
    that populates a combo box. The first item (index 0) is the default.
    Language defaults to US English if there are no translations
    available for the user's locale. It is the only setting that is not
    set back to the default by the "Reset" button.

    @author Tom Price
    @date   June 2020
    """
    variables = {
        'machine': Machine,
        'default_knitting_mode': Mode,
        'default_infinite_repeat': bool,
        'default_alignment': Alignment,
        'default_auto_mirror': bool,
        # 'default_continuous_reporting': bool,
        'quiet_mode': bool,
        'language': Language,
    }

    def __init__(self, parent):
        super().__init__(parent.seer)
        self.parent = parent
        self.languages = Language(self.parent.app_context)
        self.settings = QSettings()
        self.settings.setFallbacksEnabled(False)
        self.refresh()

    def refresh(self):
        for var in self.variables.keys():
            self.settings.setValue(var, self.value(var))

    def reset(self):
        """Reset all the fields except language"""
        for var in self.variables.keys():
            if self.variables[var] != Language:
                self.settings.setValue(var, self.default_value(var))

    def value(self, var):
        if var in self.settings.allKeys():
            try:
                return self.convert(var)(self.settings.value(var))
            except ValueError:
                # saved setting is wrong type
                return self.convert(var)()
        else:
            return self.default_value(var)

    def convert(self, var):
        try:
            cls = self.variables[var]
        except KeyError:
            return str
        # else
        if cls == bool:
            return str2bool
        # else
        if cls == Language:
            return str
        # else
        return int

    def default_value(self, var):
        try:
            cls = self.variables[var]
        except KeyError:
            return None
        # else
        if cls == bool:
            return False
        # else
        if cls == Language:
            return self.languages.default_language()
        # else
        return 0

    def open_dialog(self):
        machine_width = Machine(self.value("machine")).width
        result = PrefsDialog(self.parent).exec_()
        if machine_width != Machine(self.value("machine")).width:
            self.emit_image_resizer()


class PrefsDialog(QDialog):
    """GUI to set preferences.

    @author Tom Price
    @date   June 2020
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.__prefs = parent.prefs

        # set up preferences dialog
        self.__ui = Ui_Prefs()
        self.__ui.setupUi(self)
        self.__form = QFormLayout(self.__ui.prefs_group)

        # add form items
        self.__widget = {}
        for var in self.__prefs.variables.keys():
            self.__widget[var] = self.__make_widget(var)
            self.__form.addRow(self.__make_label(var), self.__widget[var])

        # connect dialog box buttons
        for widget in self.__widget.values():
            widget.connect()
        self.__ui.reset.clicked.connect(self.__reset_and_refresh)
        self.__ui.enter.clicked.connect(self.accept)

        # update buttons from settings
        self.__refresh_form()

    def __make_label(self, var):
        title = re.sub(r"_", r" ", var).title()
        return QLabel(QCoreApplication.translate("Prefs", title))

    def __make_widget(self, var):
        cls = self.__prefs.variables[var]
        if cls == bool:
            return PrefsBoolWidget(self.__prefs, var)
        elif cls == Language:
            return PrefsLangWidget(self.__prefs)
        else:
            return PrefsComboWidget(self.__prefs, var)

    def __refresh_form(self):
        '''Update GUI to current settings'''
        for widget in self.__widget.values():
            widget.refresh()

    def __reset_and_refresh(self):
        self.__prefs.reset()
        self.__refresh_form()


class PrefsBoolWidget(QCheckBox):
    """Checkbox for Boolean preferences setting.

    @author Tom Price
    @date   July 2020
    """
    def __init__(self, prefs, var):
        super().__init__()
        self.var = var
        self.prefs = prefs

    def connect(self):
        self.toggled.connect(self.update_setting)

    def update_setting(self):
        if self.isChecked():
            self.prefs.settings.setValue(self.var, True)
        else:
            self.prefs.settings.setValue(self.var, False)

    def refresh(self):
        if self.prefs.value(self.var):
            self.setCheckState(Qt.Checked)
        else:
            self.setCheckState(Qt.Unchecked)


class PrefsComboWidget(QComboBox):
    """ComboBox for categorical preferences setting.

    @author Tom Price
    @date   July 2020
    """
    def __init__(self, prefs, var):
        super().__init__()
        self.var = var
        self.prefs = prefs
        cls = self.prefs.variables[self.var]
        cls.add_items(self)

    def connect(self):
        self.currentIndexChanged.connect(self.update_setting)

    def update_setting(self):
        self.prefs.settings.setValue(self.var, self.currentIndex())

    def refresh(self):
        self.setCurrentIndex(self.prefs.value(self.var))


class PrefsLangWidget(QComboBox):
    """ComboBox for language setting.

    @author Tom Price
    @date   July 2020
    """
    def __init__(self, prefs):
        super().__init__()
        self.prefs = prefs
        self.prefs.languages.add_items(self)

    def connect(self):
        self.currentIndexChanged.connect(self.update_setting)

    def update_setting(self):
        self.prefs.settings.setValue("language", self.currentData())

    def refresh(self):
        self.setCurrentIndex(self.findData(self.prefs.value("language")))
