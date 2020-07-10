# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ayab_options_gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OptionsWidget(object):
    def setupUi(self, options_tab):
        options_tab.setObjectName("options_tab")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            options_tab.sizePolicy().hasHeightForWidth())
        options_tab.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget = QtWidgets.QWidget(options_tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 244, 414))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(6, 20, 12, 20)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.knitting_mode_box = QtWidgets.QComboBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.knitting_mode_box.sizePolicy().hasHeightForWidth())
        self.knitting_mode_box.setSizePolicy(sizePolicy)
        self.knitting_mode_box.setObjectName("knitting_mode_box")
        self.verticalLayout_3.addWidget(self.knitting_mode_box)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.color_edit = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.color_edit.sizePolicy().hasHeightForWidth())
        self.color_edit.setSizePolicy(sizePolicy)
        self.color_edit.setMinimum(2)
        self.color_edit.setMaximum(6)
        self.color_edit.setObjectName("color_edit")
        self.verticalLayout_3.addWidget(self.color_edit)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.start_row_edit = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.start_row_edit.sizePolicy().hasHeightForWidth())
        self.start_row_edit.setSizePolicy(sizePolicy)
        self.start_row_edit.setSuffix("")
        self.start_row_edit.setPrefix("")
        self.start_row_edit.setMinimum(1)
        self.start_row_edit.setMaximum(99999)
        self.start_row_edit.setObjectName("start_row_edit")
        self.verticalLayout_3.addWidget(self.start_row_edit)
        self.inf_repeat_checkbox = QtWidgets.QCheckBox(
            self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.inf_repeat_checkbox.sizePolicy().hasHeightForWidth())
        self.inf_repeat_checkbox.setSizePolicy(sizePolicy)
        self.inf_repeat_checkbox.setObjectName("inf_repeat_checkbox")
        self.verticalLayout_3.addWidget(self.inf_repeat_checkbox)
        self.gbox_startneedle = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.gbox_startneedle.setMinimumSize(QtCore.QSize(224, 52))
        self.gbox_startneedle.setFlat(False)
        self.gbox_startneedle.setObjectName("gbox_startneedle")
        self.start_needle_color = QtWidgets.QComboBox(self.gbox_startneedle)
        self.start_needle_color.setGeometry(QtCore.QRect(60, 20, 165, 32))
        self.start_needle_color.setObjectName("start_needle_color")
        self.start_needle_edit = QtWidgets.QSpinBox(self.gbox_startneedle)
        self.start_needle_edit.setGeometry(QtCore.QRect(0, 20, 60, 32))
        self.start_needle_edit.setPrefix("")
        self.start_needle_edit.setMinimum(1)
        self.start_needle_edit.setMaximum(100)
        self.start_needle_edit.setProperty("value", 20)
        self.start_needle_edit.setObjectName("start_needle_edit")
        self.verticalLayout_3.addWidget(self.gbox_startneedle)
        self.gbox_stopneedle = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.gbox_stopneedle.setMinimumSize(QtCore.QSize(224, 52))
        self.gbox_stopneedle.setObjectName("gbox_stopneedle")
        self.stop_needle_color = QtWidgets.QComboBox(self.gbox_stopneedle)
        self.stop_needle_color.setGeometry(QtCore.QRect(60, 20, 165, 32))
        self.stop_needle_color.setObjectName("stop_needle_color")
        self.stop_needle_edit = QtWidgets.QSpinBox(self.gbox_stopneedle)
        self.stop_needle_edit.setGeometry(QtCore.QRect(0, 20, 60, 32))
        self.stop_needle_edit.setPrefix("")
        self.stop_needle_edit.setMinimum(1)
        self.stop_needle_edit.setMaximum(100)
        self.stop_needle_edit.setProperty("value", 20)
        self.stop_needle_edit.setObjectName("stop_needle_edit")
        self.verticalLayout_3.addWidget(self.gbox_stopneedle)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.alignment_combo_box = QtWidgets.QComboBox(
            self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.alignment_combo_box.sizePolicy().hasHeightForWidth())
        self.alignment_combo_box.setSizePolicy(sizePolicy)
        self.alignment_combo_box.setObjectName("alignment_combo_box")
        self.verticalLayout_3.addWidget(self.alignment_combo_box)
        self.auto_mirror_checkbox = QtWidgets.QCheckBox(
            self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.auto_mirror_checkbox.sizePolicy().hasHeightForWidth())
        self.auto_mirror_checkbox.setSizePolicy(sizePolicy)
        self.auto_mirror_checkbox.setObjectName("auto_mirror_checkbox")
        self.verticalLayout_3.addWidget(self.auto_mirror_checkbox)
        self.continuous_reporting_checkbox = QtWidgets.QCheckBox(
            self.verticalLayoutWidget)
        self.continuous_reporting_checkbox.setObjectName(
            "continuous_reporting_checkbox")
        self.verticalLayout_3.addWidget(self.continuous_reporting_checkbox)

        self.retranslateUi(options_tab)
        QtCore.QMetaObject.connectSlotsByName(options_tab)

    def retranslateUi(self, options_tab):
        _translate = QtCore.QCoreApplication.translate
        self.label_4.setText(_translate("OptionsWidget", "Knitting Mode"))
        self.label_6.setText(_translate("OptionsWidget", "Colors"))
        self.label_5.setText(_translate("OptionsWidget", "Start Row"))
        self.inf_repeat_checkbox.setText(
            _translate("OptionsWidget", "Infinite Repeat"))
        self.gbox_startneedle.setTitle(
            _translate("OptionsWidget", "Start Needle"))
        self.gbox_stopneedle.setTitle(
            _translate("OptionsWidget", "Stop Needle"))
        self.label_3.setText(_translate("OptionsWidget", "Alignment"))
        self.auto_mirror_checkbox.setText(
            _translate("OptionsWidget", "Mirror Image"))
        self.continuous_reporting_checkbox.setText(
            _translate("OptionsWidget", "Continuous Status Reporting"))
