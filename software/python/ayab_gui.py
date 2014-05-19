import sys
import os
import serial
import serial.tools.list_ports
from PySide.QtCore import *
from PySide.QtGui  import *

from optparse import OptionParser

import ayab_image
import ayab_control


qt_app = QApplication(sys.argv)


class AYABControlGUI(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setMinimumSize(QSize(800,600))
        self.setWindowTitle("AYAB Control GUI 1.2")


        ####
        # LEFT BOX
        ####
        self.imgBox   = QVBoxLayout()
        self.imgLabel = QLabel()
        self.imgBox.addWidget(self.imgLabel)

        self.consoleBox = QVBoxLayout()
        self.imgConsoleField = QTextEdit()
        self.imgAlignmentConsoleField = QTextEdit()
        self.consoleField = QTextEdit()
        self.consoleField.setEnabled(False)
        self.consoleBox.addWidget(self.imgConsoleField)
        self.consoleBox.addWidget(self.imgAlignmentConsoleField)
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

    def mainCallback(self, pSource, pString, pType):
          if pType == "stream":
            print pString
            return
          
          if pType == "error":
            pString = "E: " + pString
          elif pType == "debug":
            pString = "D: " + pString
          elif pType == "prompt":
            pass      

          print pString
          self.consoleField.append(pString)
          
          return

    @Slot()
    def _loadImgSlot(self):        
        path, _ = QFileDialog.getOpenFileName(self, "Open File", os.getcwd())
        #self.label.setText(path)
        self.options.filename     = path
        #self.options.filename     = "../../patterns/uc3.png"
        self._loadImgFile()

    @Slot()
    def _rotateImgSlot(self):
        self._ayabImage.rotateImage()
        self._updateImgOnGui()

    @Slot()
    def _invertImgSlot(self):
        self._ayabImage.invertImage()
        self._updateImgOnGui()

    @Slot()
    def _resizeImgSlot(self):
        self._updateImgOnGui()

    @Slot()
    def _startLineChangedSlot(self):
        try:
            self._ayabImage.setStartLine(int(self.comboStartLine.currentText()))
        except:
            return

    @Slot()
    def _machineTypeChangedSlot(self):
        self.options.machine_type = self.comboMachineType.currentText()
        self._updateImgOnGui()

    @Slot()
    def _numColorsChangedSlot(self):
        self.options.num_colors = int(self.comboNumColors.currentText())
        self._ayabImage.setNumColors(self.options.num_colors)
        self._updateImgOnGui()

    @Slot()
    def _needlesChangedSlot(self):
        # TODO Error handling when setKnitNeedles fails
        try:
            self._ayabImage.setKnitNeedles(int(self.comboStartNeedle.currentText()), \
                                        int(self.comboStopNeedle.currentText()))
        except:
            return
        self._updateImgOnGui()

    @Slot()
    def _imgAlignmentChangedSlot(self):
        options.imgAlignment = self.comboAlignments.currentText()
        self._ayabImage.setImagePosition(options.imgAlignment)
        self._updateImgOnGui()

    @Slot()
    def _refreshComPorts(self):
        self.comboPorts.clear()
        self.comboPorts.addItems(self._getSerialPorts())

    @Slot()
    def _startKnitSlot(self):
        #TODO get knitting from GUI elements
        self.options.num_colors = int(self.comboNumColors.currentText())

        ayabControl = ayab_control.ayabControl(self.mainCallback)
        
        ayabControl.knitImage(self._ayabImage,self.options)


        
    def _loadImgFile(self):
        if self.options.filename == "":
            return

        try:
            self._ayabImage = ayab_image.ayabImage(options.filename)
        except:
            return

        self.comboStartLine.clear()
        for i in range(0, self._ayabImage.imgHeight()):
            self.comboStartLine.addItem(str(i))

        self.comboStartNeedle.setCurrentIndex(self._ayabImage.knitStartNeedle())
        self.comboStopNeedle.setCurrentIndex(self._ayabImage.knitStopNeedle()-1)

        self.btnRotate.setEnabled(True)
        self.btnInvert.setEnabled(True)
        #self.btnResize.setEnabled(True)
        self.comboStartLine.setEnabled(True)

        self.comboMachineType.setEnabled(True)
        self.comboNumColors.setEnabled(True)
        self.comboStartNeedle.setEnabled(True)
        self.comboStopNeedle.setEnabled(True)
        self.comboAlignments.setEnabled(True)
        self.btnStartKnit.setEnabled(True)

        #self.img = QImage(self.options.filename)
        #self.imgLabel.setPixmap(QPixmap.fromImage(self.img))

        self._updateImgOnGui()

    def _updateImgOnGui(self):
        print "_updateImgOnGui"
        imageIntern = self._ayabImage.imageIntern()

        width = self._ayabImage.imgWidth()
        height = self._ayabImage.imgHeight()

        self.lblImgName.setText(self.options.filename)
        self.lblImgWidth.setText(str(width)+ " px")
        self.lblImgHeight.setText(str(height) + " px")
        
        #setpixels
        self.imgConsoleField.clear()
        for row in range(height):
            msg = ''
            for col in range(width):
                msg += str(imageIntern[row][col])
            if row < 10:
                pre = "0"
            else:
                pre = ""
            self.imgConsoleField.append(pre + str(row) + ": " + msg)

        self.imgAlignmentConsoleField.clear()
        #show alignment
        imgStartNeedle = self._ayabImage.imgStartNeedle()
        imgStopNeedle  = self._ayabImage.imgStopNeedle()
        knitStartNeedle = self._ayabImage.knitStartNeedle()
        knitStopNeedle  = self._ayabImage.knitStopNeedle()

        # print markers for active area and knitted image
        msg = '|'
        for i in range(0,200):
            if i >= knitStartNeedle and i <= knitStopNeedle:
                if i >= imgStartNeedle and i <= imgStopNeedle:
                    msg += 'x'
                else:          
                    msg += '-'
            else:
                msg += '_'
        msg += '|'
        self.imgAlignmentConsoleField.append(msg)

        # print markers at multiples of 10
        msg = '|'
        for i in range(0,200):
            if i == 100:
                msg += '|'
            else:
                if (i % 10) == 0:
                    msg += '^'
                else:
                    msg += ' '
        msg += '|'
        self.imgAlignmentConsoleField.append(msg)
        

    def _createImgCtrlLayout(self):
        self.imgCtrlLayout = QFormLayout()

        self.lblImgName   = QLabel(self)
        self.lblImgName.setText("-")
        self.lblImgWidth  = QLabel(self)
        self.lblImgWidth.setText("-")
        self.lblImgHeight = QLabel(self)
        self.lblImgHeight.setText("-")

        self.btnLoadImage = QPushButton("Load Image", self)
        self.btnLoadImage.clicked.connect(self._loadImgSlot)
        self.btnRotate = QPushButton("Rotate", self)
        self.btnRotate.clicked.connect(self._rotateImgSlot)
        self.btnRotate.setEnabled(False)
        self.btnInvert = QPushButton("Invert", self)
        self.btnInvert.clicked.connect(self._invertImgSlot)
        self.btnInvert.setEnabled(False)
        self.btnResize = QPushButton("Resize", self)
        self.btnResize.clicked.connect(self._resizeImgSlot)
        self.btnResize.setEnabled(False)
        self.comboStartLine = QComboBox(self)
        self.comboStartLine.setEnabled(False)
        self.comboStartLine.currentIndexChanged.connect(self._startLineChangedSlot)
        
        self.imgCtrlLayout.addRow("Name", self.lblImgName)
        self.imgCtrlLayout.addRow("Width", self.lblImgWidth)
        self.imgCtrlLayout.addRow("Height", self.lblImgHeight)
        self.imgCtrlLayout.addRow(self.btnLoadImage)
        self.imgCtrlLayout.addRow(self.btnRotate)
        self.imgCtrlLayout.addRow(self.btnInvert)
        self.imgCtrlLayout.addRow(self.btnResize)
        self.imgCtrlLayout.addRow("Start Line", self.comboStartLine)

        return self.imgCtrlLayout

    def _createKnitSettingsLayout(self):
        self.knitSettingsLayout = QFormLayout()

        self.comboMachineType = QComboBox(self) 
        self.comboMachineType.setEnabled(False)       
        self.comboMachineType.addItems(['single','double'])        
        self.comboMachineType.currentIndexChanged.connect(self._machineTypeChangedSlot)

        self.comboNumColors   = QComboBox(self)
        self.comboNumColors.setEnabled(False)
        self.comboNumColors.addItems(['2','3','4','5','6'])        
        self.comboNumColors.currentIndexChanged.connect(self._numColorsChangedSlot)        

        self.comboStartNeedle = QComboBox(self)
        self.comboStartNeedle.setEnabled(False)
        self.comboStartNeedle.currentIndexChanged.connect(self._needlesChangedSlot)
        self.comboStopNeedle  = QComboBox(self)
        self.comboStopNeedle.setEnabled(False)
        self.comboStopNeedle.currentIndexChanged.connect(self._needlesChangedSlot)
        for i in range(0,199):
            self.comboStartNeedle.addItem(str(i))
        for i in range(1,200):
            self.comboStopNeedle.addItem(str(i))

        self.comboAlignments = QComboBox(self)
        self.comboAlignments.setEnabled(False)
        self.comboAlignments.addItems(['center', 'left', 'right'])
        self.comboAlignments.currentIndexChanged.connect(self._imgAlignmentChangedSlot)

        self.knitSettingsLayout.addRow("Machine Type", \
                                        self.comboMachineType)
        self.knitSettingsLayout.addRow("Colors", \
                                        self.comboNumColors)
        self.knitSettingsLayout.addRow("Start Needle", \
                                        self.comboStartNeedle)
        self.knitSettingsLayout.addRow("Stop Needle", \
                                        self.comboStopNeedle)
        self.knitSettingsLayout.addRow("Alignment", \
                                        self.comboAlignments)

        return self.knitSettingsLayout

    def _createKnitCtrlLayout(self):
        self.knitCtrlLayout = QHBoxLayout()
        self.btnPortsRefresh = QPushButton("R", self)
        self.btnPortsRefresh.clicked.connect(self._refreshComPorts)
        self.comboPorts     = QComboBox(self)
        self.comboPorts.addItems(self._getSerialPorts())
        self.btnStartKnit   = QPushButton("Start Knitting", self)
        self.btnStartKnit.clicked.connect(self._startKnitSlot)
        self.btnStartKnit.setEnabled(False)
        self.knitCtrlLayout.addWidget(self.btnPortsRefresh)
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
               if port[0].find("ACM") != -1:
                _portList.append(port[0])

        return _portList

    def run(self, options):
        self.options = options
        self.options.filename   = ""
        # TODO Initially assign these values from UI elements
        self.options.portname       = "/dev/ttyACM0"
        self.options.machine_type   = "single"
        self.options.imgAlignment   = "center"
        self.options.num_colors     = 2

        self.show()
        qt_app.exec_()

if __name__ == '__main__':
    # Parse command line options
    parser = OptionParser("%prog [filename] [options]", \
        description = "AYAB Control GUI Version")

    (options, args) = parser.parse_args()

    AYABControlGUI().run(options)

    sys.exit(0)