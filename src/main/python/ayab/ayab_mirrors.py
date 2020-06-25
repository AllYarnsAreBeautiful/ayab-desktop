# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ayab/ayab_mirrors.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MirrorDialog(object):
    def setupUi(self, mirror_dialog):
        mirror_dialog.setObjectName("mirror_dialog")
        mirror_dialog.setModal(True)
        mirror_dialog.setGeometry(QtCore.QRect(0, 0, 200, 200))
        self.mirror_vbox1 = QtWidgets.QVBoxLayout(mirror_dialog)
        self.mirror_vbox1.setObjectName("mirror_vbox1")
        self.mirror_group = QtWidgets.QGroupBox(mirror_dialog)
        self.mirror_group.setFlat(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.mirror_group.sizePolicy().hasHeightForWidth())
        self.mirror_group.setSizePolicy(sizePolicy)
        self.mirror_group.setObjectName("mirror_group")
        self.mirror_vbox2 = QtWidgets.QVBoxLayout(self.mirror_group)
        self.mirror_vbox2.setObjectName("mirror_vbox2")
        self.check0 = QtWidgets.QCheckBox(self.mirror_group)
        self.check0.setObjectName("check0")
        self.mirror_vbox2.addWidget(self.check0)
        self.check1 = QtWidgets.QCheckBox(self.mirror_group)
        self.check1.setObjectName("check1")
        self.mirror_vbox2.addWidget(self.check1)
        self.check2 = QtWidgets.QCheckBox(self.mirror_group)
        self.check2.setObjectName("check2")
        self.mirror_vbox2.addWidget(self.check2)
        self.check3 = QtWidgets.QCheckBox(self.mirror_group)
        self.check3.setObjectName("check3")
        self.mirror_vbox2.addWidget(self.check3)
        self.mirror_vbox1.addWidget(self.mirror_group)
        self.enter = QtWidgets.QPushButton(mirror_dialog)
        self.enter.setObjectName("enter")
        self.mirror_vbox1.addWidget(self.enter)

        self.retranslateUi(mirror_dialog)
        QtCore.QMetaObject.connectSlotsByName(mirror_dialog)

    def retranslateUi(self, mirror_dialog):
        _translate = QtCore.QCoreApplication.translate
        mirror_dialog.setWindowTitle(_translate("MirrorDialog", "Reflect image"))
        self.mirror_group.setTitle(_translate("MirrorDialog", "Add mirrors"))
        self.check0.setText(_translate("MirrorDialog", "Left"))
        self.check1.setText(_translate("MirrorDialog", "Right"))
        self.check2.setText(_translate("MirrorDialog", "Top"))
        self.check3.setText(_translate("MirrorDialog", "Bottom"))
        self.enter.setText(_translate("MirrorDialog", "OK"))
