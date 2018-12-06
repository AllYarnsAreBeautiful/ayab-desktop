# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'firmware_flash_ui.ui'
#
# Created: Thu Jan 26 21:52:33 2017
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FirmwareFlashFrame(object):
    def setupUi(self, FirmwareFlashFrame):
        FirmwareFlashFrame.setObjectName("FirmwareFlashFrame")
        FirmwareFlashFrame.resize(672, 493)
        FirmwareFlashFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        FirmwareFlashFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout = QtWidgets.QHBoxLayout(FirmwareFlashFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(FirmwareFlashFrame)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.widget)
        self.textBrowser.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Firmware Install Guide</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:14px; color:#333333; background-color:#ffffff;\">For Linux Users:</span><span style=\" font-family:\'Arial,sans-serif\'; font-size:14px; color:#333333;\"> <br />To be able to communicate with your Arduino, it might be necessary to add the rights for USB communication by adding your user to some groups:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f5f5f5;\"><span style=\" font-family:\'Bitstream Vera Sans Mono,DejaVu Sans Mono,Monaco,Courier,monospace\'; font-size:12px; color:#333333; background-color:#f5f5f5;\">sudo usermod -a -G tty </span><span style=\" font-family:\'Bitstream Vera Sans Mono,DejaVu Sans Mono,Monaco,Courier,monospace\'; font-size:12px; font-weight:600; color:#333333;\">[</span><span style=\" font-family:\'Bitstream Vera Sans Mono,DejaVu Sans Mono,Monaco,Courier,monospace\'; font-size:12px; color:#333333;\">userName</span><span style=\" font-family:\'Bitstream Vera Sans Mono,DejaVu Sans Mono,Monaco,Courier,monospace\'; font-size:12px; font-weight:600; color:#333333;\">]</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f5f5f5;\"><span style=\" font-family:\'Bitstream Vera Sans Mono,DejaVu Sans Mono,Monaco,Courier,monospace\'; font-size:12px; color:#333333;\">sudo usermod -a -G dialout </span><span style=\" font-family:\'Bitstream Vera Sans Mono,DejaVu Sans Mono,Monaco,Courier,monospace\'; font-size:12px; font-weight:600; color:#333333;\">[</span><span style=\" font-family:\'Bitstream Vera Sans Mono,DejaVu Sans Mono,Monaco,Courier,monospace\'; font-size:12px; color:#333333;\">userName</span><span style=\" font-family:\'Bitstream Vera Sans Mono,DejaVu Sans Mono,Monaco,Courier,monospace\'; font-size:12px; font-weight:600; color:#333333;\">]</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Arial,sans-serif\'; font-size:14px; color:#333333;\"><br /></p></body></html>")
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(FirmwareFlashFrame)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.port_combo_box = QtWidgets.QComboBox(FirmwareFlashFrame)
        self.port_combo_box.setObjectName("port_combo_box")
        self.verticalLayout.addWidget(self.port_combo_box)
        self.label_4 = QtWidgets.QLabel(FirmwareFlashFrame)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.hardware_list = QtWidgets.QListWidget(FirmwareFlashFrame)
        self.hardware_list.setObjectName("hardware_list")
        self.verticalLayout.addWidget(self.hardware_list)
        self.label = QtWidgets.QLabel(FirmwareFlashFrame)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.controller_list = QtWidgets.QListWidget(FirmwareFlashFrame)
        self.controller_list.setObjectName("controller_list")
        self.verticalLayout.addWidget(self.controller_list)
        self.label_2 = QtWidgets.QLabel(FirmwareFlashFrame)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.firmware_list = QtWidgets.QListWidget(FirmwareFlashFrame)
        self.firmware_list.setObjectName("firmware_list")
        self.verticalLayout.addWidget(self.firmware_list)
        self.flash_firmware = QtWidgets.QPushButton(FirmwareFlashFrame)
        self.flash_firmware.setObjectName("flash_firmware")
        self.verticalLayout.addWidget(self.flash_firmware)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(FirmwareFlashFrame)
        QtCore.QMetaObject.connectSlotsByName(FirmwareFlashFrame)

    def retranslateUi(self, FirmwareFlashFrame):
        _translate = QtCore.QCoreApplication.translate
        FirmwareFlashFrame.setWindowTitle(_translate("FirmwareFlashFrame", "Firmware Flashing Utility"))
        self.label_3.setText(_translate("FirmwareFlashFrame", "Port"))
        self.label_4.setText(_translate("FirmwareFlashFrame", "Hardware List"))
        self.label.setText(_translate("FirmwareFlashFrame", "Controller"))
        self.label_2.setText(_translate("FirmwareFlashFrame", "Firmware Version"))
        self.flash_firmware.setText(_translate("FirmwareFlashFrame", "Flash"))

