import sys
import os
import serial
import serial.tools.list_ports
from PySide.QtCore import *
from PySide.QtGui import *

qt_app = QApplication(sys.argv)

class AYABControlGUI(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setMinimumSize(QSize(800,600))
        self.setWindowTitle("AYAB Control GUI")


        ####
        # LEFT BOX
        ####
        self.imgBox   = QVBoxLayout()
        self.img = QImage()
        self.pixmap = QPixmap()
        self.img.

        self.consoleBox = QVBoxLayout()
        self.consoleField = QTextEdit()
        self.consoleBox.addWidget(self.consoleField)

        self.leftBox = QVBoxLayout()
        self.leftBox.addLayout(self.imgBox)
        self.leftBox.addLayout(self.consoleBox)

        ####
        # RIGHT BOX
        ####
        self._createImgCtrlLayout()
        self._createKnitSettingsLayout()
        self._createKnitCtrlLayout()

        self.rightBox = QVBoxLayout()
        self.rightBox.addStretch(1)
        self.rightBox.addLayout(self.imgCtrlLayout)
        self.rightBox.addStretch(1)
        self.rightBox.addLayout(self.knitSettingsLayout)
        self.rightBox.addLayout(self.knitCtrlLayout)

        ####
        # MAIN LAYOUT
        ####
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.leftBox)
        self.layout.addLayout(self.rightBox)

        self.setLayout(self.layout)

    def _createImgCtrlLayout(self):
        self.imgCtrlLayout = QFormLayout()
        self.btnLoadImage = QPushButton("Load Image", self)
        self.btnRotate = QPushButton("Rotate", self)
        self.btnInvert = QPushButton("Invert", self)
        self.btnResize = QPushButton("Resize", self)
        self.comboStartLine = QComboBox(self)
        for i in range(10):
            self.comboStartLine.addItem(str(i))
        
        self.imgCtrlLayout.addRow(self.btnLoadImage)
        self.imgCtrlLayout.addRow(self.btnRotate)
        self.imgCtrlLayout.addRow(self.btnInvert)
        self.imgCtrlLayout.addRow(self.btnResize)
        self.imgCtrlLayout.addRow("Start Line", self.comboStartLine)

        return self.imgCtrlLayout

    def _createKnitSettingsLayout(self):
        self.knitSettingsLayout = QFormLayout()
        self.comboStartNeedle = QComboBox(self)
        self.comboStopNeedle  = QComboBox(self)
        for i in range(0,199):
            self.comboStartNeedle.addItem(str(i))
        for i in range(1,200):
            self.comboStopNeedle.addItem(str(i))

        self.alignments = ['left', 'center', 'right']
        self.comboAlignments = QComboBox(self)
        self.comboAlignments.addItems(self.alignments)


        self.knitSettingsLayout.addRow("Start Needle", self.comboStartNeedle)
        self.knitSettingsLayout.addRow("Stop Needle", self.comboStopNeedle)
        self.knitSettingsLayout.addRow("Alignment", self.comboAlignments)

        return self.knitSettingsLayout

    def _createKnitCtrlLayout(self):
        self.knitCtrlLayout = QHBoxLayout()
        self.comboPorts = QComboBox(self)
        self.comboPorts.addItems(self._getSerialPorts())
        self.btnStartKnit = QPushButton("Start Knitting", self)
        self.knitCtrlLayout.addWidget(self.comboPorts)
        self.knitCtrlLayout.addWidget(self.btnStartKnit)

        return self.knitCtrlLayout


    def _getSerialPorts(self):
        """
        Returns a list of all available serial ports
        """
        _portList = []
        if os.name == 'nt':
            # windows
            for i in range(256):
                try:
                    s = serial.Serial(i)
                    s.close()
                    _portList.append('COM' + str(i + 1))
                except serial.SerialException:
                    pass
        else:
            # unix
            for port in serial.tools.list_ports.comports():
               _portList.append(port[0])

        return _portList

    def run(self):
        self.show()
        qt_app.exec_()

AYABControlGUI().run()