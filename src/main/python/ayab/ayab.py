# -*- coding: utf-8 -*-
# This file is part of AYAB.
#
#    AYAB is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AYAB is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with AYAB.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright 2014 Sebastian Oliva, Christian Obersteiner, Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

"""Provides an Interface for users to operate AYAB using a GUI."""
from fbs_runtime.application_context.PyQt5 import ApplicationContext

import sys
from os import path, mkdir
import logging
from bitarray import bitarray
import numpy as np

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QState, QObject, QThread, pyqtSignal

from PIL import Image

from .ayab_gui import Ui_MainWindow
from .ayab_about import Ui_AboutForm
from .ayab_fsm import FSM
from .ayab_scene import Scene
from .ayab_preferences import Preferences, str2bool
from .plugins.ayab_plugin import AyabPlugin
from .plugins.ayab_plugin.firmware_flash import FirmwareFlash
from .plugins.ayab_plugin.ayab_progress import KnitProgress
from .plugins.ayab_plugin.ayab_control import KnittingMode, Progress

# Temporal serial imports.
import serial
import serial.tools.list_ports

# from playsound import playsound

# TODO move to generic configuration
MACHINE_WIDTH = 200

userdata_path = path.expanduser(path.join("~", "AYAB"))
if not path.isdir(userdata_path):
    mkdir(userdata_path)

logfile = path.join(userdata_path, "ayab_log.txt")
logging.basicConfig(filename=logfile,
                    level=logging.DEBUG,
                    format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s',
                    datefmt='%y-%m-%d %H:%M:%S')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(
    logging.Formatter('%(asctime)s %(name)-8s %(levelname)-8s %(message)s'))
logging.getLogger().addHandler(console)

# Fix PyQt5 for HiDPI screens
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
# Remove Help Button
if hasattr(Qt, 'AA_DisableWindowContextHelpButton'):
    QtWidgets.QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton, True)

    
class GuiMain(QMainWindow):
    """GuiMain is the main object that handles the instance of AYAB's GUI from ayab_gui.UiForm .

    GuiMain inherits from QMainWindow and instantiates a window with the form components form ayab_gui.UiForm.
    """
    signalUpdateProgressBar = pyqtSignal(int, int, int)
    signalUpdateColorSymbol = pyqtSignal('QString')
    signalUpdateStatus = pyqtSignal(int, int, 'QString', int)
    signalUpdateNotification = pyqtSignal('QString')
    signalDisplayPopUp = pyqtSignal('QString', 'QString')
    signalDisplayBlockingPopUp = pyqtSignal('QString', 'QString')
    signalPlaysound = pyqtSignal('QString')
    signalUpdateButtonKnitEnabled = pyqtSignal(bool)
    signalUpdateWidgetKnitControlEnabled = pyqtSignal(bool)
    signalResetKnitProgress = pyqtSignal()
    signalUpdateKnitProgress = pyqtSignal(Progress, int)
    signalUpdateNeedles = pyqtSignal(int, int)
    signalUpdateAlignment = pyqtSignal('QString')
    signalImageLoaded = pyqtSignal()
    signalImageTransformed = pyqtSignal()
    signalConfigured = pyqtSignal()
    signalDoneKnitProgress = pyqtSignal()
    signalDoneKnitting = pyqtSignal()

    def __init__(self, app_context):
        super(GuiMain, self).__init__(None)

        self.app_context = app_context

        self.image_file_route = None
    
        self.prefs = Preferences()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__setupMenuBar()
        self.scene = Scene(self)
        self.kp = KnitProgress(self.ui)
        self.plugin = AyabPlugin()
        self.plugin.setupUi(self)

        # set initial knitting configuration options
        knitting_mode_box = self.plugin.ui.knitting_mode_box
        knitting_mode_box.setCurrentIndex(knitting_mode_box.findText(self.prefs.settings.value("default_knitting_mode")))
        if str2bool(self.prefs.settings.value("default_infinite_repeat")):
            self.plugin.ui.infRepeat_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.plugin.ui.infRepeat_checkbox.setCheckState(QtCore.Qt.Unchecked)
        if str2bool(self.prefs.settings.value("automatic_mirroring")):
            self.plugin.ui.autoMirror_checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.plugin.ui.autoMirror_checkbox.setCheckState(QtCore.Qt.Unchecked)
        self.scene.imageAlignment = self.prefs.settings.value("default_alignment")
        alignment_combo_box = self.plugin.ui.alignment_combo_box
        alignment_combo_box.setCurrentIndex(alignment_combo_box.findText(self.scene.imageAlignment))
        
        self.showMaximized()
        self.__setup_behavior()

        # clear progress and status bar
        self.ui.label_notifications.setText("")
        self.resetProgressBar()

        # initialize FSM
        self.fs = FSM(self)
        self.fs.transitions()
        self.fs.properties()
        self.fs.machine.start()

    def resetProgressBar(self):
        self.ui.label_current_row.setText("")
        self.ui.label_current_color.setText("")

    def updateProgressBar(self, row, total=0, repeats=0):
        '''Updates the Progress Bar.'''
        if row < 0:
            return

        # Store to local variable
        self.var_progress = row
        self.scene.refresh()

        # Update label
        if total == 0:
            text = ""
        else:
            text = "Row {0}/{1}".format(row, total)
            if repeats >= 0:
                text += " ({0} repeats completed)".format(repeats)
        self.ui.label_current_row.setText(text)
        
        self.plugin.ui.label_progress.setText("{0}/{1}".format(row, total))

    def updateColorSymbol(self, colorSymbol):
        '''Updates the current color symbol.'''
        if colorSymbol == "":
            text = ""
        else:
            text = "Color " + colorSymbol
        self.ui.label_current_color.setText(text)
            
    def updateStatus(self, hall_l, hall_r, carriage_type, carriage_position):
        self.plugin.ui.progress_hall_l.setValue(hall_l)
        self.plugin.ui.label_hall_l.setText(str(hall_l))
        self.plugin.ui.progress_hall_r.setValue(hall_r)
        self.plugin.ui.label_hall_r.setText(str(hall_r))
        self.plugin.ui.slider_position.setValue(carriage_position)
        self.plugin.ui.label_carriage.setText(carriage_type)
        
    def updateNotification(self, text):
        '''Updates the Notification field'''
        logging.info("Notification: " + text)
        self.ui.label_notifications.setText(text)

    def slotPlaysound(self, event):
        return
        # if event == "start":
        #     playsound(self.app_context.get_resource("assets/start.wav"))
        # if event == "nextline":
        #     playsound(self.app_context.get_resource("assets/nextline.wav"))
        # if event == "finished":
        #     playsound(self.app_context.get_resource("assets/finish.wav"))

    def updateWidgetKnitControlEnabled(self, enabled):
        self.ui.widget_knitcontrol.setEnabled(enabled)        
    
    def updateButtonKnitEnabled(self, enabled):
        self.ui.knit_button.setEnabled(enabled)

    def displayBlockingPopUp(self, message="", message_type="info"):
        logging.debug("MessageBox {}: '{}'".format(message_type, message))
        box_function = {
            "error": QtWidgets.QMessageBox.critical,
            "info": QtWidgets.QMessageBox.information,
            "question": QtWidgets.QMessageBox.question,
            "warning": QtWidgets.QMessageBox.warning
        }
        message_box_function = box_function.get(message_type)

        ret = message_box_function(
            self,
            "AYAB",
            message,
            QtWidgets.QMessageBox.Ok,
            QtWidgets.QMessageBox.Ok)
        if ret == QtWidgets.QMessageBox.Ok:
            return True

    def resetKnitProgress(self):
        '''Reset knit progress frame.'''
        self.kp.reset()

    def updateKnitProgress(self, progress, row_multiplier):
        self.kp.update(progress, row_multiplier)
        if progress.current_row > 0 and progress.current_row == progress.total_rows:
            self.signalDoneKnitProgress.emit()

    def wheelEvent(self, event):
        self.scene.zoom(event)

    def __setup_behavior(self):
        # UI actions
        self.ui.load_file_button.clicked.connect(self.file_select_dialog)
        self.ui.filename_lineedit.returnPressed.connect(self.file_select_dialog)
        self.ui.cancel_button.clicked.connect(self.plugin.cancel)
        self.ui.actionLoad_AYAB_Firmware.triggered.connect(self.generate_firmware_ui)
        self.ui.image_pattern_view.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

        # Menu actions
        self.ui.actionSetPreferences.triggered.connect(self.set_preferences)
        self.ui.actionAbout.triggered.connect(self.open_about_ui)
        self.ui.actionQuit.triggered.connect(QtCore.QCoreApplication.instance().quit)
        self.ui.actionInvert.triggered.connect(self.scene.invert_image)
        self.ui.actionStretch.triggered.connect(self.scene.stretch_image)
        self.ui.actionRepeat.triggered.connect(self.scene.repeat_image)
        self.ui.actionReflect.triggered.connect(self.scene.reflect_image)
        self.ui.actionHorizontalFlip.triggered.connect(self.scene.hflip_image)
        self.ui.actionVerticalFlip.triggered.connect(self.scene.vflip_image)
        self.ui.actionRotateLeft.triggered.connect(self.scene.rotate_left)
        self.ui.actionRotateRight.triggered.connect(self.scene.rotate_right)

        # Signal actions
        self.signalUpdateProgressBar.connect(self.updateProgressBar)
        self.signalUpdateColorSymbol.connect(self.updateColorSymbol)
        self.signalUpdateStatus.connect(self.updateStatus)
        self.signalUpdateNotification.connect(self.updateNotification)
        self.signalPlaysound.connect(self.slotPlaysound)
        self.signalUpdateWidgetKnitControlEnabled.connect(self.updateWidgetKnitControlEnabled)
        self.signalUpdateButtonKnitEnabled.connect(self.updateButtonKnitEnabled)
        self.signalDisplayBlockingPopUp.connect(self.displayBlockingPopUp)
        self.signalDisplayPopUp.connect(self.displayBlockingPopUp)
        self.signalResetKnitProgress.connect(self.resetKnitProgress)
        self.signalUpdateKnitProgress.connect(self.updateKnitProgress)
        self.signalUpdateNeedles.connect(self.scene.updateNeedles)
        self.signalUpdateAlignment.connect(self.scene.updateAlignment)

    def start_knitting_process(self):
        # disable UI elements at start of knitting
        self.__depopulateMenuBar()
        self.ui.filename_lineedit.setEnabled(False)        
        self.ui.load_file_button.setEnabled(False)
        self.ui.widget_optionsdock.setEnabled(False)
        # start thread for knit plugin
        self.gt = GenericThread(self.plugin.knit)
        self.gt.start()

    def reset_ui_after_knitting(self):
        # (Re-)enable UI elements after knitting finishes
        self.__repopulateMenuBar()
        self.ui.filename_lineedit.setEnabled(True)        
        self.ui.load_file_button.setEnabled(True)
        self.ui.widget_optionsdock.setEnabled(True)

    def __setupMenuBar(self):
        self.__actionImageActions = self.ui.menuImageActions.menuAction()
        self.__actionTools = self.ui.menuTools.menuAction()
        self.__actionPreferences = self.ui.menuPreferences.menuAction()
        self.__actionHelp = self.ui.menuHelp.menuAction()
        self.ui.menubar.addAction(self.__actionTools)
        self.ui.menubar.addAction(self.__actionPreferences)
        self.ui.menubar.addAction(self.__actionHelp)

    def __depopulateMenuBar(self):
        try:
            self.ui.menubar.removeAction(self.__actionImageActions)
        except:
            pass
        self.ui.menubar.removeAction(self.__actionTools)

    def __repopulateMenuBar(self):
        self.ui.menubar.removeAction(self.__actionPreferences)
        self.ui.menubar.removeAction(self.__actionHelp)
        self.ui.menubar.addAction(self.__actionImageActions)
        self.ui.menubar.addAction(self.__actionTools)
        self.ui.menubar.addAction(self.__actionPreferences)
        self.ui.menubar.addAction(self.__actionHelp)

    def addImageActions(self):
        # This workaround is necessary because 
        # self.__actionImageActions.setEnabled(True)
        # does not seems to work (at least, not on Ubuntu 16.04)
        # Tom Price June 2020
        self.__depopulateMenuBar()
        self.__repopulateMenuBar()

    def file_select_dialog(self):
        filenameValue = self.ui.filename_lineedit.text()
        if filenameValue == '':
            filePath = self.app_context.get_resource("patterns")
        else:
            filePath = filenameValue
        file_selected_route, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open file", filePath, 'Images (*.png *.PNG *.jpg *.JPG *.jpeg *.JPEG *.bmp *.BMP *.gif *.GIF *.tiff *.TIFF *.tif *.TIF *.Pat *.pat *.PAT *.Stp *.stp *.STP)')
        if file_selected_route:
            self.__update_file_selected_text_field(file_selected_route)
            self.__load_image_from_string(str(file_selected_route))

    def __update_file_selected_text_field(self, route):
        '''Sets self.image_file_route and ui.filename_lineedit to route.'''
        self.ui.filename_lineedit.setText(route)
        self.image_file_route = route

    def __load_image_from_string(self, image_str):
        '''Loads an image into self.ui.image_pattern_view using a temporary QGraphicsScene'''
        # TODO Check maximum width of image
        try:
            self.scene.load_image_file(image_str)
        except OSError:
            logging.error("unable to load " + str(image_str))
        except Exception as e:
            logging.error(e)
        else:
            self.scene.refresh()
            self.signalImageLoaded.emit()
            self.statusBar().showMessage(image_str)
            # Tell loaded plugin elements about changed parameters
            width, height = self.scene.image.size
            self.plugin.setImageDimensions(width, height)

    def generate_firmware_ui(self):
        self.__flash_ui = FirmwareFlash(self)
        self.__flash_ui.show()

    def open_about_ui(self):
        __version__ = "package_version"
        filename_version = self.app_context.get_resource("ayab/package_version")
        with open(filename_version) as version_file:
            __version__ = version_file.read().strip()
        
        self.__AboutForm = QtWidgets.QFrame()
        self.__about_ui = Ui_AboutForm()
        self.__about_ui.setupUi(self.__AboutForm)
        self.__about_ui.label_3.setText("Version " + __version__)
        self.__AboutForm.show()

    def set_preferences(self):
        return self.prefs.setPrefsDialog()

    def getSerialPorts(self):
        """
        Returns a list of all USB Serial Ports
        """
        return list(serial.tools.list_ports.grep("USB"))


class GenericThread(QThread):
    '''A generic thread wrapper for functions on threads.'''

    def __init__(self, function, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        #self.join()
        self.wait()

    def run(self):
        try:
            self.function(*self.args, **self.kwargs)
        except Exception:
            for arg in self.args:
                print(arg)
            for key, value in self.kwargs.items():
                print(key, value)
            raise


def run(app_context):
    translator = QtCore.QTranslator()
    ## Loading ayab_gui main translator.
    translator.load(QtCore.QLocale.system(), "ayab_gui", ".", app_context.get_resource("ayab/translations"), ".qm")
    app = QtWidgets.QApplication(sys.argv)
    app.installTranslator(translator)
    window = GuiMain(app_context)
    window.show()
    sys.exit(app.exec_())
