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
from yapsy import PluginManager
from PIL import ImageQt
from fysom import FysomError

from ayab_gui import Ui_Form


logging.basicConfig(level=logging.DEBUG)


class GuiMain(QtGui.QWidget):
    def __init__(self):
        super(GuiMain, self).__init__(None)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.plugins_init()
        self.setupBehaviour()

        self.image_file_route = None
        self.enabled_plugin = None

    def plugins_init(self, is_reloading=False):
        if is_reloading:
          logging.info("Deactivating All Plugins")
          for pluginInfo in self.pm.getAllPlugins():
            self.pm.deactivatePluginByName(pluginInfo.name)
        if getattr(sys, 'frozen', False):
            route = sys._MEIPASS
            logging.info("loading from pyinstaller")
            self.pm = PluginManager.PluginManager(directories_list=[os.path.join(route, "plugins")],)
        else:
            plugins_folder = os.path.join(os.path.dirname(__file__),"plugins")
            print(plugins_folder)
            self.pm = PluginManager.PluginManager(directories_list=[plugins_folder],)

        self.pm.collectPlugins()
        for pluginInfo in self.pm.getAllPlugins():
          ## This stops the plugins marked as Disabled from being activated.
          if (not pluginInfo.details.has_option("Core", "Disabled")):
            plugin_name = pluginInfo.name
            self.pm.activatePluginByName(plugin_name)
            self.add_plugin_name_on_module_dropdown(plugin_name)
            logging.info("Plugin {0} activated".format(plugin_name))

    def add_plugin_name_on_module_dropdown(self, module_name):
        self.ui.module_dropdown.addItem(module_name)

    def set_enabled_plugin(self, plugin_name=None):
        """Enables plugin, sets up gui and returns the plugin_object from the plugin selected on module_dropdown."""
        if self.enabled_plugin:
            self.enabled_plugin.plugin_object.cleanup_ui(self)

        if not plugin_name:
            plugin_name = window.ui.module_dropdown.currentText()
        plugin_o = self.pm.getPluginByName(plugin_name)
        self.enabled_plugin = plugin_o

        self.enabled_plugin.plugin_object.setup_ui(self)
        logging.info("Set enabled_plugin as {0} - {1}".format(plugin_o, plugin_name))
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
        self.ui.load_file_button.clicked.connect(self.file_select_dialog)
        self.ui.module_dropdown.activated[str].connect(self.set_enabled_plugin)
        self.ui.knit_button.clicked.connect(self.start_knitting_process)
        self.connect(self, QtCore.SIGNAL("updateProgress(int)"), self.updateProgress)
        # This blocks the other thread until signal is done
        self.connect(self, QtCore.SIGNAL("display_blocking_pop_up_signal(QString, QString)"), self.display_blocking_pop_up, QtCore.Qt.BlockingQueuedConnection)
        self.connect(self, QtCore.SIGNAL("display_blocking_pop_up_signal(QString)"), self.display_blocking_pop_up, QtCore.Qt.BlockingQueuedConnection)

    def load_image_on_scene(self, image_str):
        """Loads an image into self.ui.image_pattern_view using a temporary QGraphicsScene"""
        self.__pil_image = ImageQt.Image.open(image_str)
        self.__qt_image = ImageQt.ImageQt(self.__pil_image)
        self.__qpixmap = QtGui.QPixmap.fromImage(self.__qt_image)
        self.__qscene = QtGui.QGraphicsScene()
        self.__qscene.addPixmap(self.__qpixmap)

        #l = QtCore.QLineF(0,0,100,100)
        #self.__qscene.addLine(l)

        qv = self.ui.image_pattern_view
        qv.setScene(self.__qscene)

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
        self.enabled_plugin.plugin_object.configure(parent_ui=self)

    def file_select_dialog(self):
        file_selected_route = QtGui.QFileDialog.getOpenFileName(self)
        self.update_file_selected_text_field(file_selected_route)
        self.load_image_on_scene(str(file_selected_route))


class GenericThread(QtCore.QThread):
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

def run():
  app = QtGui.QApplication(sys.argv)
  window = GuiMain()
  window.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  run()
