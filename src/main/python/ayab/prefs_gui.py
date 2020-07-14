# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ayab_prefs_gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PrefsDialog(object):
    def setupUi(self, prefs_dialog):
        prefs_dialog.setObjectName("prefs_dialog")
        prefs_dialog.setModal(True)
        self.prefs_grid = QtWidgets.QGridLayout(prefs_dialog)
        self.prefs_grid.setObjectName("prefs_grid")
        self.prefs_group = QtWidgets.QGroupBox(prefs_dialog)
        self.prefs_group.setFlat(True)
        self.prefs_group.setObjectName("prefs_group")
        self.prefs_grid.addWidget(self.prefs_group, 0, 0, 1, 5)
        self.enter = QtWidgets.QPushButton(prefs_dialog)
        self.enter.setObjectName("enter")
        self.prefs_grid.addWidget(self.enter, 1, 0, 1, 1)
        self.reset = QtWidgets.QPushButton(prefs_dialog)
        self.reset.setObjectName("reset")
        self.prefs_grid.addWidget(self.reset, 1, 4, 1, 1)

        self.retranslateUi(prefs_dialog)
        QtCore.QMetaObject.connectSlotsByName(prefs_dialog)

    def retranslateUi(self, prefs_dialog):
        _translate = QtCore.QCoreApplication.translate
        prefs_dialog.setWindowTitle(
            _translate("PrefsDialog", "Set Preferences"))
        self.prefs_group.setTitle(_translate("PrefsDialog", "Settings"))
        self.enter.setText(_translate("PrefsDialog", "OK"))
        self.reset.setText(_translate("PrefsDialog", "Reset"))
