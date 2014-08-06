# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'firmware_flash_ui.ui'
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

class Ui_FirmwareFlashFrame(object):
    def setupUi(self, FirmwareFlashFrame):
        FirmwareFlashFrame.setObjectName(_fromUtf8("FirmwareFlashFrame"))
        FirmwareFlashFrame.resize(672, 493)
        FirmwareFlashFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        FirmwareFlashFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.horizontalLayout = QtGui.QHBoxLayout(FirmwareFlashFrame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget = QtGui.QWidget(FirmwareFlashFrame)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.textBrowser = QtGui.QTextBrowser(self.widget)
        self.textBrowser.setHtml(_fromUtf8("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Firmware Install Guide</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,sans-serif\'; font-size:14px; color:#333333; background-color:#ffffff;\">For Linux Users:</span><span style=\" font-family:\'Arial,sans-serif\'; font-size:14px; color:#333333;\"> <br />To be able to communicate with your Arduino, it might be necessary to add the rights for USB communication by adding your user to some groups:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f5f5f5;\"><span style=\" font-family:\'Bitstream Vera Sans Mono,DejaVu Sans Mono,Monaco,Courier,monospace\'; font-size:12px; color:#333333; background-color:#f5f5f5;\">sudo usermod -a -G tty </span><span style=\" font-family:\'Bitstream Vera Sans Mono,DejaVu Sans Mono,Monaco,Courier,monospace\'; font-size:12px; font-weight:600; color:#333333;\">[</span><span style=\" font-family:\'Bitstream Vera Sans Mono,DejaVu Sans Mono,Monaco,Courier,monospace\'; font-size:12px; color:#333333;\">userName</span><span style=\" font-family:\'Bitstream Vera Sans Mono,DejaVu Sans Mono,Monaco,Courier,monospace\'; font-size:12px; font-weight:600; color:#333333;\">]</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f5f5f5;\"><span style=\" font-family:\'Bitstream Vera Sans Mono,DejaVu Sans Mono,Monaco,Courier,monospace\'; font-size:12px; color:#333333;\">sudo usermod -a -G dialout </span><span style=\" font-family:\'Bitstream Vera Sans Mono,DejaVu Sans Mono,Monaco,Courier,monospace\'; font-size:12px; font-weight:600; color:#333333;\">[</span><span style=\" font-family:\'Bitstream Vera Sans Mono,DejaVu Sans Mono,Monaco,Courier,monospace\'; font-size:12px; color:#333333;\">userName</span><span style=\" font-family:\'Bitstream Vera Sans Mono,DejaVu Sans Mono,Monaco,Courier,monospace\'; font-size:12px; font-weight:600; color:#333333;\">]</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Arial,sans-serif\'; font-size:14px; color:#333333;\"><br /></p></body></html>"))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QtGui.QLabel(FirmwareFlashFrame)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.port_combo_box = QtGui.QComboBox(FirmwareFlashFrame)
        self.port_combo_box.setObjectName(_fromUtf8("port_combo_box"))
        self.verticalLayout.addWidget(self.port_combo_box)
        self.label_4 = QtGui.QLabel(FirmwareFlashFrame)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.hardware_list = QtGui.QListWidget(FirmwareFlashFrame)
        self.hardware_list.setObjectName(_fromUtf8("hardware_list"))
        self.verticalLayout.addWidget(self.hardware_list)
        self.label = QtGui.QLabel(FirmwareFlashFrame)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.controller_list = QtGui.QListWidget(FirmwareFlashFrame)
        self.controller_list.setObjectName(_fromUtf8("controller_list"))
        self.verticalLayout.addWidget(self.controller_list)
        self.label_2 = QtGui.QLabel(FirmwareFlashFrame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.firmware_list = QtGui.QListWidget(FirmwareFlashFrame)
        self.firmware_list.setObjectName(_fromUtf8("firmware_list"))
        self.verticalLayout.addWidget(self.firmware_list)
        self.flash_firmware = QtGui.QPushButton(FirmwareFlashFrame)
        self.flash_firmware.setObjectName(_fromUtf8("flash_firmware"))
        self.flash_firmware.setEnabled(False)
        self.verticalLayout.addWidget(self.flash_firmware)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(FirmwareFlashFrame)
        QtCore.QMetaObject.connectSlotsByName(FirmwareFlashFrame)

    def retranslateUi(self, FirmwareFlashFrame):
        FirmwareFlashFrame.setWindowTitle(_translate("FirmwareFlashFrame", "Firmware Flashing Utility", None))
        self.label_3.setText(_translate("FirmwareFlashFrame", "Port", None))
        self.label_4.setText(_translate("FirmwareFlashFrame", "Hardware List", None))
        self.label.setText(_translate("FirmwareFlashFrame", "Controller", None))
        self.label_2.setText(_translate("FirmwareFlashFrame", "Firmware Version", None))
        self.flash_firmware.setText(_translate("FirmwareFlashFrame", "Flash", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FirmwareFlashFrame = QtGui.QFrame()
    ui = Ui_FirmwareFlashFrame()
    ui.setupUi(FirmwareFlashFrame)
    FirmwareFlashFrame.show()
    sys.exit(app.exec_())

