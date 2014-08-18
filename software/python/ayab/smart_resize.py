# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'smart_resize.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(668, 331)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 4, 4, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 4, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.vertical_stitches_label = QtGui.QLabel(Dialog)
        self.vertical_stitches_label.setText(_fromUtf8(""))
        self.vertical_stitches_label.setObjectName(_fromUtf8("vertical_stitches_label"))
        self.gridLayout.addWidget(self.vertical_stitches_label, 2, 5, 1, 1)
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 4, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 5, 5, 1, 1)
        self.calculated_height_label = QtGui.QLabel(Dialog)
        self.calculated_height_label.setText(_fromUtf8(""))
        self.calculated_height_label.setObjectName(_fromUtf8("calculated_height_label"))
        self.gridLayout.addWidget(self.calculated_height_label, 4, 5, 1, 1)
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 4, 1, 1)
        self.ratio_label = QtGui.QLabel(Dialog)
        self.ratio_label.setText(_fromUtf8(""))
        self.ratio_label.setObjectName(_fromUtf8("ratio_label"))
        self.gridLayout.addWidget(self.ratio_label, 0, 2, 1, 1)
        self.ratios_list = QtGui.QListWidget(Dialog)
        self.ratios_list.setObjectName(_fromUtf8("ratios_list"))
        self.gridLayout.addWidget(self.ratios_list, 1, 3, 5, 1)
        self.width_spinbox = QtGui.QDoubleSpinBox(Dialog)
        self.width_spinbox.setObjectName(_fromUtf8("width_spinbox"))
        self.gridLayout.addWidget(self.width_spinbox, 2, 2, 1, 1)
        self.label_8 = QtGui.QLabel(Dialog)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 3)
        self.calculated_width_label = QtGui.QLabel(Dialog)
        self.calculated_width_label.setText(_fromUtf8(""))
        self.calculated_width_label.setObjectName(_fromUtf8("calculated_width_label"))
        self.gridLayout.addWidget(self.calculated_width_label, 3, 5, 1, 1)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 3, 4, 1, 1)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 4, 1, 1)
        self.height_spinbox = QtGui.QDoubleSpinBox(Dialog)
        self.height_spinbox.setObjectName(_fromUtf8("height_spinbox"))
        self.gridLayout.addWidget(self.height_spinbox, 3, 2, 1, 1)
        self.horizontal_stitches_label = QtGui.QLabel(Dialog)
        self.horizontal_stitches_label.setText(_fromUtf8(""))
        self.horizontal_stitches_label.setObjectName(_fromUtf8("horizontal_stitches_label"))
        self.gridLayout.addWidget(self.horizontal_stitches_label, 1, 5, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_3.setText(_translate("Dialog", "Calculated Height", None))
        self.label_2.setText(_translate("Dialog", "Calculated Horizontal Stitches", None))
        self.label.setText(_translate("Dialog", "Ratio", None))
        self.label_7.setText(_translate("Dialog", "Physical Height", None))
        self.label_6.setText(_translate("Dialog", "Proposed Aproximate Ratios", None))
        self.label_9.setText(_translate("Dialog", "Physical Width", None))
        self.label_8.setText(_translate("Dialog", "Input Width and Height in cm", None))
        self.label_5.setText(_translate("Dialog", "Calculated Width", None))
        self.label_4.setText(_translate("Dialog", "Calculated Vertical Stitches", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

