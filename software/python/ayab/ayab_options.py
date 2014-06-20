# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ayab_options.ui'
#
# Created by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(223, 436)
        self.ayab_config = QtGui.QWidget(Form)
        self.ayab_config.setGeometry(QtCore.QRect(10, 10, 164, 391))
        self.ayab_config.setObjectName(_fromUtf8("ayab_config"))
        self.verticalLayout = QtGui.QVBoxLayout(self.ayab_config)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_5 = QtGui.QLabel(self.ayab_config)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.start_line_edit = QtGui.QLineEdit(self.ayab_config)
        self.start_line_edit.setObjectName(_fromUtf8("start_line_edit"))
        self.verticalLayout.addWidget(self.start_line_edit)
        self.label = QtGui.QLabel(self.ayab_config)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.start_needle_edit = QtGui.QLineEdit(self.ayab_config)
        self.start_needle_edit.setObjectName(_fromUtf8("start_needle_edit"))
        self.verticalLayout.addWidget(self.start_needle_edit)
        self.label_2 = QtGui.QLabel(self.ayab_config)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.stop_needle_edit = QtGui.QLineEdit(self.ayab_config)
        self.stop_needle_edit.setObjectName(_fromUtf8("stop_needle_edit"))
        self.verticalLayout.addWidget(self.stop_needle_edit)
        self.label_3 = QtGui.QLabel(self.ayab_config)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.alignment_combo_box = QtGui.QComboBox(self.ayab_config)
        self.alignment_combo_box.setObjectName(_fromUtf8("alignment_combo_box"))
        self.verticalLayout.addWidget(self.alignment_combo_box)
        self.label_4 = QtGui.QLabel(self.ayab_config)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.machine_type_box = QtGui.QComboBox(self.ayab_config)
        self.machine_type_box.setObjectName(_fromUtf8("machine_type_box"))
        self.machine_type_box.addItem(_fromUtf8(""))
        self.machine_type_box.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.machine_type_box)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_5.setText(_translate("Form", "Start Line", None))
        self.start_line_edit.setText(_translate("Form", "0", None))
        self.label.setText(_translate("Form", "Start Needle", None))
        self.start_needle_edit.setText(_translate("Form", "0", None))
        self.label_2.setText(_translate("Form", "Stop Needle", None))
        self.stop_needle_edit.setText(_translate("Form", "0", None))
        self.label_3.setText(_translate("Form", "Alignment", None))
        self.label_4.setText(_translate("Form", "Machine Type", None))
        self.machine_type_box.setItemText(0, _translate("Form", "Single", None))
        self.machine_type_box.setItemText(1, _translate("Form", "Double", None))

