# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ayab/ayab_prefs_gui.ui'
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
        self.prefs_form = QtWidgets.QGridLayout(self.prefs_group)
        self.prefs_form.setObjectName("prefs_form")
        self.default_knitting_mode_label = QtWidgets.QLabel(self.prefs_group)
        self.default_knitting_mode_label.setObjectName("default_knitting_mode_label")
        self.prefs_form.addWidget(self.default_knitting_mode_label, 0, 0, 1, 1)
        self.default_knitting_mode_box = QtWidgets.QComboBox(self.prefs_group)
        self.default_knitting_mode_box.setObjectName("default_knitting_mode_box")
        self.default_knitting_mode_box.addItem("")
        self.default_knitting_mode_box.setItemText(0, "Singlebed")
        self.default_knitting_mode_box.addItem("")
        self.default_knitting_mode_box.setItemText(1, "Ribber: Classic")
        self.default_knitting_mode_box.addItem("")
        self.default_knitting_mode_box.setItemText(2, "Ribber: Middle-Colors-Twice")
        self.default_knitting_mode_box.addItem("")
        self.default_knitting_mode_box.setItemText(3, "Ribber: Heart of Pluto")
        self.default_knitting_mode_box.addItem("")
        self.default_knitting_mode_box.setItemText(4, "Ribber: Circular")
        self.prefs_form.addWidget(self.default_knitting_mode_box, 0, 1, 1, 1)
        self.default_infinite_repeat_label = QtWidgets.QLabel(self.prefs_group)
        self.default_infinite_repeat_label.setObjectName("default_infinite_repeat_label")
        self.prefs_form.addWidget(self.default_infinite_repeat_label, 1, 0, 1, 1)
        self.default_infinite_repeat_checkbox = QtWidgets.QCheckBox(self.prefs_group)
        self.default_infinite_repeat_checkbox.setObjectName("default_infinite_repeat_checkbox")
        self.prefs_form.addWidget(self.default_infinite_repeat_checkbox, 1, 1, 1, 1)
        self.default_alignment_label = QtWidgets.QLabel(self.prefs_group)
        self.default_alignment_label.setObjectName("default_alignment_label")
        self.prefs_form.addWidget(self.default_alignment_label, 2, 0, 1, 1)
        self.default_alignment_box = QtWidgets.QComboBox(self.prefs_group)
        self.default_alignment_box.setObjectName("default_alignment_box")
        self.default_alignment_box.addItem("")
        self.default_alignment_box.setItemText(0, "center")
        self.default_alignment_box.addItem("")
        self.default_alignment_box.setItemText(1, "left")
        self.default_alignment_box.addItem("")
        self.default_alignment_box.setItemText(2, "right")
        self.prefs_form.addWidget(self.default_alignment_box, 2, 1, 1, 1)
        self.automatic_mirroring_label = QtWidgets.QLabel(self.prefs_group)
        self.automatic_mirroring_label.setObjectName("automatic_mirroring_label")
        self.prefs_form.addWidget(self.automatic_mirroring_label, 3, 0, 1, 1)
        self.automatic_mirroring_checkbox = QtWidgets.QCheckBox(self.prefs_group)
        self.automatic_mirroring_checkbox.setObjectName("automatic_mirroring_checkbox")
        self.prefs_form.addWidget(self.automatic_mirroring_checkbox, 3, 1, 1, 1)
        self.quiet_mode_label = QtWidgets.QLabel(self.prefs_group)
        self.quiet_mode_label.setObjectName("quiet_mode_label")
        self.prefs_form.addWidget(self.quiet_mode_label, 4, 0, 1, 1)
        self.quiet_mode_checkbox = QtWidgets.QCheckBox(self.prefs_group)
        self.quiet_mode_checkbox.setObjectName("quiet_mode_checkbox")
        self.prefs_form.addWidget(self.quiet_mode_checkbox, 4, 1, 1, 1)
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
        prefs_dialog.setWindowTitle(_translate("PrefsDialog", "Set Preferences"))
        self.prefs_group.setTitle(_translate("PrefsDialog", "Settings"))
        self.default_knitting_mode_label.setText(_translate("PrefsDialog", "Default Knitting Mode"))
        self.default_infinite_repeat_label.setText(_translate("PrefsDialog", "Default Infinite Repeat"))
        self.default_alignment_label.setText(_translate("PrefsDialog", "Default Alignment"))
        self.automatic_mirroring_label.setText(_translate("PrefsDialog", "Default Mirroring"))
        self.quiet_mode_label.setText(_translate("PrefsDialog", "Quiet Mode"))
        self.enter.setText(_translate("PrefsDialog", "OK"))
        self.reset.setText(_translate("PrefsDialog", "Reset"))
