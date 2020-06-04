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
from os import path, mkdir
from shutil import copy


def str2bool(s):
    return s.lower() == "true"

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
        self.dialog = None

    def reset(self):
        '''Reset preferences to default values'''
        self.settings.setValue("automatic_mirroring",False)
        self.settings.setValue("default_knitting_mode","Singlebed")
        self.settings.setValue("default_infinite_repeat",False)
        self.settings.setValue("default_alignment","center")

    def refresh(self):
        '''Update preferences GUI to current values'''
        self.default_knitting_mode_box.setCurrentIndex(self.default_knitting_mode_box.findText(self.settings.value("default_knitting_mode")))
        if self.settings.value("default_infinite_repeat"):
            self.default_infinite_repeat_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.default_infinite_repeat_checkbox.setCheckState(QtCore.Qt.Unchecked)
        self.default_alignment_box.setCurrentIndex(self.default_alignment_box.findText(self.settings.value("default_alignment")))
        if self.settings.value("automatic_mirroring"):
            self.automatic_mirroring_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.automatic_mirroring_checkbox.setCheckState(QtCore.Qt.Unchecked)

    def setPrefsDialog(self):
        '''GUI to set preferences'''
        self.dialog = QtWidgets.QDialog()
        self.dialog.setWindowTitle("Set Preferences")
        self.dialog.setWindowModality(Qt.ApplicationModal)

        self.default_knitting_mode_box = QtWidgets.QComboBox()
        self.default_knitting_mode_box.addItem("Singlebed")
        self.default_knitting_mode_box.addItem("Ribber: Classic")
        self.default_knitting_mode_box.addItem("Ribber: Middle-Colors-Twice")
        self.default_knitting_mode_box.addItem("Ribber: Heart of Pluto")
        self.default_knitting_mode_box.addItem("Ribber: Circular")
        self.default_knitting_mode_box.currentIndexChanged.connect(self.__update_default_knitting_mode_setting)
        vbox1 = QtWidgets.QVBoxLayout()
        vbox1.setContentsMargins(3,3,3,3)
        vbox1.addWidget(self.default_knitting_mode_box)
        group1 = QtWidgets.QGroupBox("Default Knitting Mode")
        group1.setLayout(vbox1)
        group1.setFlat(True)

        self.default_infinite_repeat_checkbox = QtWidgets.QCheckBox("Default Infinite Repeat")
        self.default_infinite_repeat_checkbox.toggled.connect(self.__toggle_default_infinite_repeat_setting)

        self.default_alignment_box = QtWidgets.QComboBox()
        self.default_alignment_box.addItem("center")
        self.default_alignment_box.addItem("left")
        self.default_alignment_box.addItem("right")
        self.default_alignment_box.currentIndexChanged.connect(self.__update_default_alignment_setting)
        vbox2 = QtWidgets.QVBoxLayout()
        vbox2.setContentsMargins(3,3,3,3)
        vbox2.addWidget(self.default_alignment_box)
        group2 = QtWidgets.QGroupBox("Default Alignment")
        group2.setLayout(vbox2)
        group2.setFlat(True)

        self.automatic_mirroring_checkbox = QtWidgets.QCheckBox("Automatic Mirroring")
        self.automatic_mirroring_checkbox.toggled.connect(self.__toggle_automatic_mirroring_setting)
        # disable checkbox because this option is not implemented yet
        self.automatic_mirroring_checkbox.setEnabled(False)

        reset = QtWidgets.QPushButton("Reset")
        reset.clicked.connect(self.__reset_and_refresh)
        enter = QtWidgets.QPushButton("OK")
        enter.clicked.connect(self.dialog.accept)
        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(3,3,3,3)
        hbox.addWidget(enter)
        hbox.addWidget(reset)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(10)
        layout.addWidget(group1)
        layout.addWidget(self.default_infinite_repeat_checkbox)
        layout.addWidget(group2)
        layout.addWidget(self.automatic_mirroring_checkbox)
        group = QtWidgets.QGroupBox("Preferences")
        group.setLayout(layout)
        group.setFlat(True)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(group)
        grid.addLayout(hbox,1,0,2,1)
        self.dialog.setLayout(grid)

        self.refresh()
        return self.dialog.exec_()

    def __update_default_knitting_mode_setting(self):
        self.settings.setValue("default_knitting_mode",
                               self.default_knitting_mode_box.itemText(self.default_knitting_mode_box.currentIndex()))

    def __toggle_default_infinite_repeat_setting(self):
        self.settings.setValue("default_infinite_repeat",
                               not self.settings.value("default_infinite_repeat"))

    def __update_default_alignment_setting(self):
        self.settings.setValue("default_alignment",
                               self.default_alignment_box.itemText(self.default_alignment_box.currentIndex()))

    def __toggle_automatic_mirroring_setting(self):
        self.settings.setValue("automatic_mirroring",
                               not self.settings.value("automatic_mirroring"))

    def __reset_and_refresh(self):
        self.reset()
        self.refresh()
