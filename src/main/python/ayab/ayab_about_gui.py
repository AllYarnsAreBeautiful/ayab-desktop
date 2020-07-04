# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ayab/ayab_about.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
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
        self.title_label = QtWidgets.QLabel(AboutForm)
        self.title_label.setObjectName("title_label")
        self.verticalLayout.addWidget(self.title_label)
        self.link_label = QtWidgets.QLabel(AboutForm)
        self.link_label.setObjectName("link_label")
        self.verticalLayout.addWidget(self.link_label)
        self.manual_label = QtWidgets.QLabel(AboutForm)
        self.manual_label.setObjectName("manual_label")
        self.verticalLayout.addWidget(self.manual_label)
        spacerItem = QtWidgets.QSpacerItem(20, 40,
                                           QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(AboutForm)
        QtCore.QMetaObject.connectSlotsByName(AboutForm)

    def retranslateUi(self, AboutForm):
        _translate = QtCore.QCoreApplication.translate
        AboutForm.setWindowTitle(_translate("AboutForm", "About AYAB"))
        self.title_label.setText(
            _translate("AboutForm", "All Yarns Are Beautiful"))
        self.link_label.setText(
            _translate(
                "AboutForm",
                "<html><head/><body><p><a href=\"http://ayab-knitting.com\"><span style=\" text-decoration: underline; color:#0000ff;\">http://ayab-knitting.com</span></a></p></body></html>"
            ))


from . import resources_rc
