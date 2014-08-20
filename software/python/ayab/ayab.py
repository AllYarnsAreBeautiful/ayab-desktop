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
#    Copyright 2014 Sebastian Oliva, Christian Obersteiner, Andreas Müller
#    https://bitbucket.org/chris007de/ayab-apparat/

"""Provides an Interface for users to operate AYAB using a GUI."""

import sys
import os
import logging

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import QThread

from yapsy import PluginManager
from PIL import ImageQt
from PIL import Image
from fysom import FysomError

from ayab_gui import Ui_MainWindow
from plugins.ayab_plugin.firmware_flash import FirmwareFlash
from ayab_about import Ui_AboutForm

## Temporal serial imports.
import serial
import serial.tools.list_ports


logging.basicConfig(level=logging.DEBUG)


class GuiMain(QMainWindow):
    """GuiMain is the main object that handles the instance of AYAB's GUI from ayab_gui.UiForm .

    GuiMain inherits from QMainWindow and instanciates a window with the form components form ayab_gui.UiForm.
    """

    def __init__(self):
        super(GuiMain, self).__init__(None)

        self.image_file_route = None
        self.enabled_plugin = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.plugins_init()
        self.setupBehaviour()

    def plugins_init(self, is_reloading=False):
        if is_reloading:
          logging.info("Deactivating All Plugins")
          for pluginInfo in self.pm.getAllPlugins():
            self.pm.deactivatePluginByName(pluginInfo.name)
        route = get_route()
        self.pm = PluginManager.PluginManager(directories_list=[os.path.join(route, "plugins")],)

        self.pm.collectPlugins()
        for pluginInfo in self.pm.getAllPlugins():
          ## This stops the plugins marked as Disabled from being activated.
          if (not pluginInfo.details.has_option("Core", "Disabled")):
            plugin_name = pluginInfo.name
            self.pm.activatePluginByName(plugin_name)
            self.add_plugin_name_on_module_dropdown(plugin_name)
            logging.info("Plugin {0} activated".format(plugin_name))
        ## Setting AYAB as the default value
        ## TODO: better way of setting ayab as default plugin.
        self.set_enabled_plugin("AYAB")

    def add_plugin_name_on_module_dropdown(self, module_name):
        self.ui.module_dropdown.addItem(module_name)

    def set_enabled_plugin(self, plugin_name=None):
        """Enables plugin, sets up gui and returns the plugin_object from the plugin selected on module_dropdown."""
        try:
          if self.enabled_plugin:
            self.enabled_plugin.plugin_object.cleanup_ui(self)
        except:
          pass

        if not plugin_name:
            plugin_name = self.ui.module_dropdown.currentText()
        plugin_o = self.pm.getPluginByName(plugin_name)
        self.enabled_plugin = plugin_o

        try:
            self.enabled_plugin.plugin_object.setup_ui(self)
            logging.info("Set enabled_plugin as {0} - {1}".format(plugin_o, plugin_name))
        except:
            logging.info("no plugin object loaded")
        return plugin_o

    def updateProgress(self, progress):
        '''Updates the Progress Bar.'''
        self.ui.progressBar.setValue(progress)

    def update_file_selected_text_field(self, route):
        ''''Sets self.image_file_route and ui.filename_lineedit to route.'''
        self.ui.filename_lineedit.setText(route)
        self.image_file_route = route

    def start_knitting_process(self):
        self.gt = GenericThread(self.enabled_plugin.plugin_object.knit, parent_window=self)
        self.gt.start()

    def setupBehaviour(self):
        # Connecting UI elements.
        self.ui.load_file_button.clicked.connect(self.file_select_dialog)
        self.ui.module_dropdown.activated[str].connect(self.set_enabled_plugin)
        self.ui.knit_button.clicked.connect(self.start_knitting_process)
        self.ui.actionLoad_AYAB_Firmware.activated.connect(self.generate_firmware_ui)
        self.ui.image_pattern_view.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        # Connecting Signals.
        self.connect(self, QtCore.SIGNAL("updateProgress(int)"), self.updateProgress)
        self.connect(self, QtCore.SIGNAL("display_pop_up_signal(QString, QString)"), self.display_blocking_pop_up)
        # This blocks the other thread until signal is done
        self.connect(self, QtCore.SIGNAL("display_blocking_pop_up_signal(QString, QString)"), self.display_blocking_pop_up, QtCore.Qt.BlockingQueuedConnection)
        self.connect(self, QtCore.SIGNAL("display_blocking_pop_up_signal(QString)"), self.display_blocking_pop_up, QtCore.Qt.BlockingQueuedConnection)
        self.ui.actionQuit.activated.connect(QtCore.QCoreApplication.instance().quit)
        self.ui.actionAbout.activated.connect(self.open_about_ui)
        self.ui.actionMirror.activated.connect(self.mirror_image)
        self.ui.actionInvert.activated.connect(self.invert_image)
        self.ui.actionRotate_Left.activated.connect(self.rotate_left)
        self.ui.actionRotate_Right.activated.connect(self.rotate_right)
        self.ui.actionVertical_Flip.activated.connect(self.flip_image)
        self.ui.actionSmart_Resize.activated.connect(self.smart_resize)

    def load_image_from_string(self, image_str):
        """Loads an image into self.ui.image_pattern_view using a temporary QGraphicsScene"""
        self.pil_image = Image.open(image_str)
        self.load_pil_image_on_scene(self.pil_image)

    def load_pil_image_on_scene(self, image_obj):
        '''Loads the PIL image on a QtScene and sets it as the current scene on the Image View.'''
        width, height = image_obj.size
        self.__qt_image = ImageQt.ImageQt(image_obj)
        self.__qpixmap = QtGui.QPixmap.fromImage(self.__qt_image)
        self.__qscene = QtGui.QGraphicsScene()
        self.__qscene.addPixmap(self.__qpixmap)

        #l = QtCore.QLineF(0,0,100,100)
        #self.__qscene.addLine(l)

        self.set_dimensions_on_gui(width, height)



        qv = self.ui.image_pattern_view
        qv.resetTransform()
        qv.scale(2.0, 2.0)
        qv.setScene(self.__qscene)

    def set_dimensions_on_gui(self, width, height):
        text = u"{} - {}".format(width, height)
        self.ui.dimensions_label.setText(text)

    def display_blocking_pop_up(self, message="", message_type="info"):
        logging.debug("message emited: '{}'".format(message))
        box_function = {
            "info": QtGui.QMessageBox.information,
            "warning": QtGui.QMessageBox.warning,
            "error": QtGui.QMessageBox.critical,
        }
        message_box_function = box_function.get(message_type, QtGui.QMessageBox.warning)
        ret = message_box_function(
            self,
            "AYAB",
            message,
            QtGui.QMessageBox.AcceptRole,
            QtGui.QMessageBox.AcceptRole)
        if ret == QtGui.QMessageBox.AcceptRole:
            return True

    def conf_button_function(self):
        self.enabled_plugin.plugin_object.configure(self)

    def file_select_dialog(self):
        file_selected_route = QtGui.QFileDialog.getOpenFileName(self)
        self.update_file_selected_text_field(file_selected_route)
        self.load_image_from_string(str(file_selected_route))

    def generate_firmware_ui(self):
      self.__flash_ui = FirmwareFlash(self)
      self.__flash_ui.show()

    def open_about_ui(self):
        self.__AboutForm = QtGui.QFrame()
        self.__about_ui = Ui_AboutForm()
        self.__about_ui.setupUi(self.__AboutForm)
        self.__AboutForm.show()

    def invert_image(self):
        '''Public invert current Image function.'''
        self.apply_image_transform("invert")

    def mirror_image(self):
        '''Public mirror current Image function.'''
        self.apply_image_transform("mirror")

    def flip_image(self):
        '''Public mirror current Image function.'''
        self.apply_image_transform("flip")

    def rotate_left(self):
        '''Public rotate left current Image function.'''
        self.apply_image_transform("rotate", -90.0)

    def rotate_right(self):
        '''Public rotate right current Image function.'''
        self.apply_image_transform("rotate", 90.0)

    def smart_resize(self):
      '''Executes the smart resize process including dialog .'''
      dialog_result = self.__launch_get_start_smart_resize_dialog_result(self)
      if dialog_result:
        self.apply_image_transform("smart_resize", dialog_result)

    def apply_image_transform(self, transform_type, *args):
        '''Executes an image transform specified by key and args.

        Calls a function from transform_dict, forwarding args and the image,
        and replaces the QtImage on scene.
        '''
        transform_dict = {
            'invert': self.__invert_image,
            'mirror': self.__mirror_image,
            'flip': self.__flip_image,
            'rotate': self.__rotate_image,
            'smart_resize': self.__smart_resize_image,
        }
        transform = transform_dict.get(transform_type)
        image = self.pil_image
        if not image:
            return
        # Executes the transform function
        try:
          image = transform(image, args)
        except:
          logging.error("Error on executing transform")
        # Update the view
        self.pil_image = image
        self.load_pil_image_on_scene(self.pil_image)

    def __smart_resize_image(self, image, args):
      '''Implement the smart resize processing. Ratio sent as a tuple of horizontal and vertical values.'''
      import knit_aware_resize
      wratio, hratio = args[0]  # Unpacks the first argument.
      logging.debug("resizing image with args: {0}".format(args))
      resized_image = knit_aware_resize.resize_image(image, wratio, hratio)
      return resized_image

    def __rotate_image(self, image, args):
        if not args:
            logging.debug("image not altered on __rotate_image.")
            return image
        rotated_image = image.rotate(args[0], expand=True)
        return rotated_image

    def __invert_image(self, image, args):
        import PIL.ImageChops
        inverted_image = PIL.ImageChops.invert(image)
        return inverted_image

    def __mirror_image(self, image, args):
        import PIL.ImageOps
        mirrored_image = PIL.ImageOps.mirror(image)
        return mirrored_image

    def __flip_image(self, image, args):
        import PIL.ImageOps
        flipped_image = PIL.ImageOps.flip(image)
        return flipped_image

    def __launch_get_start_smart_resize_dialog_result(self, parent):
        '''Processes dialog and returns a ratio tuple or False.'''
        import smart_resize
        import knit_aware_resize
        ##TODO: create smart_resize dialog
        ## Show dialog
        self.physical_width, self.physical_height = 0.0, 0.0
        self.ratio_tuple = 1.0, 1.0
        ratio = 0.0
        dialog = QtGui.QDialog()
        dialog.ui = smart_resize.Ui_Dialog()
        dialog.ui.setupUi(dialog)

        def calculate_ratio_value(height, width):
          '''Calculates the ratio value with given height and width.'''
          try:
            return height / width
          except:
            return 0.0

        def set_ratio_list(ratio):
          '''Sets the dialog ratio list to a list of aproximations of rational ratios that match it.'''
          dialog.ui.ratios_list.clear()
          self.ratio_list = knit_aware_resize.get_rational_ratios(ratio)
          for ratio in self.ratio_list:
            ratio_string = "{0:.0f} - {1:.0f}".format(ratio[0], ratio[1])
            dialog.ui.ratios_list.addItem(ratio_string)

        def set_ratio_value(ratio):
          dialog.ui.ratio_label.setText(u"{0:.2f}".format(ratio))
          set_ratio_list(ratio)

        def recalculate_ratio():
          ratio = calculate_ratio_value(self.physical_height, self.physical_width)
          set_ratio_value(ratio)
          logging.debug("Set Ratio to {}".format(ratio))

        def set_height_ratio(height_string):
          self.physical_height = float(height_string)
          recalculate_ratio()

        def set_width_ratio(width_string):
          self.physical_width = float(width_string)
          recalculate_ratio()

        def get_ratios_list_item_value(selected_value):
          '''Gets the value of the tuple corresponding to the selected ratio list.'''
          try:
            self.ratio_tuple = self.ratio_list[selected_value]
            recalculate_real_size(self.ratio_tuple)
            logging.debug(self.ratio_tuple)
          except IndexError:
            pass

        def recalculate_real_size(ratio_tuple):
          '''Updates the calculations on the Resize dialog.'''
          try:
            h, w = self.pil_image.size
            h_ratio, w_ratio = ratio_tuple
            horizontal_size_text, vertical_size_text = u"{0:.2f}".format(h * h_ratio), u"{0:.2f}".format(w * w_ratio)
            dialog.ui.horizontal_stitches_label.setText(horizontal_size_text)
            dialog.ui.vertical_stitches_label.setText(vertical_size_text)
            real_width_text, real_height_text = unicode(self.physical_height * h_ratio), unicode(self.physical_width * w_ratio)
            dialog.ui.calculated_width_label.setText(real_width_text)
            dialog.ui.calculated_height_label.setText(real_height_text)
          except:
            pass

        dialog.ui.height_spinbox.valueChanged[unicode].connect(set_height_ratio)
        dialog.ui.width_spinbox.valueChanged[unicode].connect(set_width_ratio)
        dialog.ui.ratios_list.currentRowChanged[int].connect(get_ratios_list_item_value)

        dialog_ok = dialog.exec_()
        #dialog.show()

        logging.debug(dialog_ok)
        if dialog_ok:
          print ratio
          return self.ratio_tuple
          #set variables to parent
        else:
          return False

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
        except FysomError as fe:
            logging.error(fe)
            parent = self.kwargs["parent_window"]
            parent.emit(QtCore.SIGNAL('display_blocking_pop_up_signal(QString, QString)'), QtGui.QApplication.translate("Form",
                        "Error on plugin action, be sure to configure before starting Knitting.", None), "error")
        return


def get_route():
  #if getattr(sys, 'frozen', False):
  #  route = sys._MEIPASS
  #  logging.debug("Loading AYAB from pyinstaller.")
  #  return route
  #else:
    filename = os.path.dirname(__file__)
    logging.debug("Loading AYAB from normal package structure.")
    return filename


def run():
  translator = QtCore.QTranslator()
  ## Loading ayab_gui main translator.
  translator.load(QtCore.QLocale.system(), "ayab_gui", ".", os.path.join(get_route(), "translations"), ".qm")
  app = QtGui.QApplication(sys.argv)
  app.installTranslator(translator)
  window = GuiMain()
  window.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  run()
