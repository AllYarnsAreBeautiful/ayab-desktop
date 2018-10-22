# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ayab_about.ui'
#
# Created: Thu Jan 26 21:51:16 2017
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutForm(object):
    def setupUi(self, AboutForm):
        AboutForm.setObjectName("AboutForm")
        AboutForm.resize(583, 354)
        AboutForm.setAutoFillBackground(False)
        AboutForm.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.verticalLayout = QtWidgets.QVBoxLayout(AboutForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AboutForm)
        font = QtGui.QFont()
        font.setPointSize(144)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/ayab_logo.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(AboutForm)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_4 = QtWidgets.QLabel(AboutForm)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_3 = QtWidgets.QLabel(AboutForm)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(AboutForm)
        QtCore.QMetaObject.connectSlotsByName(AboutForm)

    def retranslateUi(self, AboutForm):
        _translate = QtCore.QCoreApplication.translate
        AboutForm.setWindowTitle(_translate("AboutForm", "About AYAB"))
        self.label_2.setText(_translate("AboutForm", "All Yarns Are Beautiful"))
        self.label_4.setText(_translate("AboutForm", "<html><head/><body><p><a href=\"http://ayab-knitting.com\"><span style=\" text-decoration: underline; color:#0000ff;\">http://ayab-knitting.com</span></a></p></body></html>"))
        self.label_3.setText(_translate("AboutForm", "Version PACKAGE_VERSION"))

from . import resources_rc
