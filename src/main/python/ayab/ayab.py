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

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog, QInputDialog, QDialog
from PyQt5.QtCore import Qt, QTranslator, QThread, QLocale, QCoreApplication, QSettings

import simpleaudio as sa
import wave

from .ayab_gui import Ui_MainWindow
from .ayab_fsm import FSM
from .ayab_menu import Menu
from .ayab_scene import Scene
from .ayab_mailbox import SignalReceiver
from .ayab_preferences import Preferences, str2bool
from .ayab_progress import Progress, ProgressBar
from .ayab_about import About
from .ayab_knitprogress import KnitProgress
from .plugins.ayab_plugin import AyabPlugin
from .plugins.ayab_plugin.firmware_flash import FirmwareFlash
from .plugins.ayab_plugin.ayab_options import Alignment
from .plugins.ayab_plugin.machine import Machine

# TODO move to generic configuration

userdata_path = path.expanduser(path.join("~", "AYAB"))
if not path.isdir(userdata_path):
    mkdir(userdata_path)

logfile = path.join(userdata_path, "ayab_log.txt")
logging.basicConfig(
    filename=logfile,
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
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
# Remove Help Button
if hasattr(Qt, 'AA_DisableWindowContextHelpButton'):
    QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton, True)


class GuiMain(QMainWindow):
    """GuiMain is the main object that handles the instance of AYAB's GUI from ayab_gui.UiForm .

    GuiMain inherits from QMainWindow and instantiates a window with the form components form ayab_gui.UiForm.
    """
    def __init__(self, app_context):
        super(GuiMain, self).__init__(None)
        self.app_context = app_context

        self.image_file_route = None

        # get preferences
        self.prefs = Preferences(app_context)

        # create UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.menu = Menu(self)
        self.menu.setup()
        self.mailbox = SignalReceiver()
        self.scene = Scene(self)
        self.about = About(app_context)
        self.plugin = AyabPlugin()
        self.plugin.setupUi(self)
        self.progress = Progress()
        self.pb = ProgressBar(self)
        self.kp = KnitProgress(self.ui)
        self.gt = GenericThread(self.plugin.knit)

        # set default knitting configuration options
        defaults = self.prefs.settings
        self.plugin.ui.knitting_mode_box.setCurrentIndex(
            defaults.value("default_knitting_mode"))
        if str2bool(defaults.value("default_infinite_repeat")):
            self.plugin.ui.infRepeat_checkbox.setCheckState(Qt.Checked)
        else:
            self.plugin.ui.infRepeat_checkbox.setCheckState(Qt.Unchecked)
        if str2bool(defaults.value("automatic_mirroring")):
            self.plugin.ui.autoMirror_checkbox.setCheckState(Qt.Checked)
        else:
            self.plugin.ui.autoMirror_checkbox.setCheckState(Qt.Unchecked)
        self.plugin.ui.alignment_combo_box.setCurrentIndex(
            self.scene.alignment.value)

        # clear progress and status bar
        self.reset_notification()
        self.pb.reset()

        # show UI
        self.showMaximized()

        # connect signals and UI actions to slots
        self.mailbox.connect_slots(self)
        self.__connect_ui_actions()
        self.__connect_menu_actions()

        # initialize FSM
        self.fs = FSM()
        self.fs.set_transitions(self)
        self.fs.set_properties(self.ui)
        self.fs.machine.start()

    def update_start_row(self, start_row):
        self.progress.row = start_row
        self.pb.refresh()
        self.scene.row_progress = start_row

    def set_image_dimensions(self):
        """Set dimensions on GUI"""
        width, height = self.scene.image.size
        self.plugin.set_image_dimensions(width, height)
        self.progress.row = self.scene.row_progress + 1
        self.progress.total = height
        self.pb.refresh()
        self.update_notification(
            QCoreApplication.translate("Scene", "Image dimensions") +
            ": {} x {}".format(width, height), False)
        self.scene.refresh()

    def update_progress(self, row, total, repeats, color_symbol):
        self.progress.update(row, total, repeats, color_symbol)
        self.pb.refresh()

    def update_status_tab(self, hall_l, hall_r, carriage_type,
                          carriage_position):
        self.plugin.ui.progress_hall_l.setValue(hall_l)
        self.plugin.ui.label_hall_l.setText(str(hall_l))
        self.plugin.ui.progress_hall_r.setValue(hall_r)
        self.plugin.ui.label_hall_r.setText(str(hall_r))
        self.plugin.ui.slider_position.setValue(carriage_position)
        self.plugin.ui.label_carriage.setText(carriage_type)

    def reset_notification(self):
        '''Updates the Notification field'''
        self.ui.label_notifications.setText("")

    def update_notification(self, text, log):
        '''Updates the Notification field'''
        if log:
            logging.info("Notification: " + text)
        self.ui.label_notifications.setText(text)

    def display_blocking_popup(self, message="", message_type="info"):
        logging.debug("MessageBox {}: '{}'".format(message_type, message))
        box_function = {
            "error": QMessageBox.critical,
            "info": QMessageBox.information,
            "question": QMessageBox.question,
            "warning": QMessageBox.warning
        }
        message_box_function = box_function.get(message_type)

        ret = message_box_function(self, "AYAB", message, QMessageBox.Ok,
                                   QMessageBox.Ok)
        if ret == QMessageBox.Ok:
            return True

    def update_knit_progress(self, status, row_multiplier):
        self.kp.update(status, row_multiplier)
        # if status.current_row > 0 and status.current_row == status.total_rows:
        #     self.mailbox.done_knit_progress.emit()

    def wheelEvent(self, event):
        self.scene.zoom = event

    def __connect_ui_actions(self):
        # UI actions
        self.ui.load_file_button.clicked.connect(self.open_file_select_dialog)
        self.ui.filename_lineedit.returnPressed.connect(
            self.open_file_select_dialog)
        self.ui.cancel_button.clicked.connect(self.plugin.cancel)

    def __connect_menu_actions(self):
        self.menu.ui.action_load_AYAB_firmware.triggered.connect(
            self.generate_firmware_ui)
        self.menu.ui.action_set_preferences.triggered.connect(
            self.open_preferences_dialog)
        self.menu.ui.action_about.triggered.connect(self.about.show)
        self.menu.ui.action_quit.triggered.connect(
            QCoreApplication.instance().quit)
        self.menu.ui.action_invert.triggered.connect(self.scene.invert_image)
        self.menu.ui.action_stretch.triggered.connect(self.scene.stretch_image)
        self.menu.ui.action_repeat.triggered.connect(self.scene.repeat_image)
        self.menu.ui.action_reflect.triggered.connect(self.scene.reflect_image)
        self.menu.ui.action_horizontal_flip.triggered.connect(
            self.scene.hflip_image)
        self.menu.ui.action_vertical_flip.triggered.connect(
            self.scene.vflip_image)
        self.menu.ui.action_rotate_left.triggered.connect(
            self.scene.rotate_left)
        self.menu.ui.action_rotate_right.triggered.connect(
            self.scene.rotate_right)

    def start_knitting_process(self):
        # reset knit progress window
        self.kp.reset()
        # disable UI elements at start of knitting
        self.menu.depopulate()
        self.ui.filename_lineedit.setEnabled(False)
        self.ui.load_file_button.setEnabled(False)
        # start thread for knit plugin
        self.gt.start()

    def reset_ui_after_knitting(self, audio: bool):
        # (Re-)enable UI elements after knitting finishes
        self.menu.repopulate()
        self.ui.filename_lineedit.setEnabled(True)
        self.ui.load_file_button.setEnabled(True)
        if audio:
            self.__audio("finish")

    def open_file_select_dialog(self):
        filenameValue = self.ui.filename_lineedit.text()
        if filenameValue == '':
            filePath = self.app_context.get_resource("patterns")
        else:
            filePath = filenameValue
        file_selected_route, _ = QFileDialog.getOpenFileName(
            self, "Open file", filePath,
            'Images (*.png *.PNG *.jpg *.JPG *.jpeg *.JPEG *.bmp *.BMP *.gif *.GIF *.tiff *.TIFF *.tif *.TIF *.Pat *.pat *.PAT *.Stp *.stp *.STP)'
        )
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
        except (OSError, FileNotFoundError):
            logging.error("unable to load " + str(image_str))
        except Exception as e:
            logging.error(e)
        else:
            self.scene.refresh()
            self.mailbox.image_loaded_flagger.emit()
            self.statusBar().showMessage(image_str)
            self.set_image_dimensions()

    def generate_firmware_ui(self):
        self.__flash_ui = FirmwareFlash(self)
        self.__flash_ui.show()

    def open_preferences_dialog(self):
        return self.prefs.set_prefs_dialog()

    def audio(self, sound):
        """Blocking -- call from external thread only"""
        self.__audio(sound)

    def __audio(self, sound):
        """Play audio and wait until finished"""
        if str2bool(self.prefs.settings.value("quiet_mode")):
            return
        dirname = self.app_context.get_resource("assets")
        filename = sound + ".wav"
        try:
            wave_read = wave.open(path.join(dirname, filename), 'rb')
        except FileNotFoundError:
            logging.warning("File " + filename + " not found.")
        except OSError:
            logging.warning("Error loading " + filename + ".")
        else:
            wave_obj = sa.WaveObject.from_wave_read(wave_read)
            play_obj = wave_obj.play()
            play_obj.wait_done()


class GenericThread(QThread):
    '''A generic thread wrapper for functions on threads.'''
    def __init__(self, function, *args, **kwargs):
        QThread.__init__(self)
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
    # set constants for QSettings
    QCoreApplication.setOrganizationName("AYAB")
    QCoreApplication.setOrganizationDomain("ayab-knitting.com")
    QCoreApplication.setApplicationName("ayab")

    # load translators
    translator = QTranslator()
    lang_dir = app_context.get_resource("ayab/translations")
    try:
        language = QSettings().value("language")
    except Exception:
        language = None
    try:
        translator.load("ayab_trans." + language, lang_dir)
    except (TypeError, FileNotFoundError):
        logging.warning(
            "Unable to load translation file for preferred language, using default locale"
        )
        try:
            translator.load(QLocale.system(), "ayab_trans", "", lang_dir)
        except Exception:
            logging.warning(
                "Unable to load translation file for default locale, using American English"
            )
            translator.load("ayab_trans.en_US", lang_dir)
    except Exception:
        logging.error("Unable to load translation file")
        raise
    app = QApplication(sys.argv)
    app.installTranslator(translator)

    # execute app
    window = GuiMain(app_context)
    window.show()
    sys.exit(app.exec_())
