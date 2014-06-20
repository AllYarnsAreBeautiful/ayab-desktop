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
import logging
from PyQt4 import QtGui, QtCore
from ayab_gui import Ui_Form

from yapsy.PluginManager import PluginManager
from plugins.knitting_plugin import KnittingPlugin


logging.basicConfig(level=logging.DEBUG)


class GuiMain(QtGui.QWidget):
    def __init__(self):
        super(GuiMain, self).__init__(None)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setupBehaviour()
        self.plugins_init()

        self.image_file_route = None

    def plugins_init(self, is_reloading=False):
        if is_reloading:
          logging.info("Deactivating All Plugins")
          for pluginInfo in self.pm.getAllPlugins():
            self.pm.deactivatePluginByName(pluginInfo.name)

        self.pm = PluginManager(directories_list=["plugins"],)

        self.pm.collectPlugins()
        for pluginInfo in self.pm.getAllPlugins():
          ## This stops the plugins marked as Disabled from being activated.
          if (not pluginInfo.details.has_option("Core", "Disabled")):
            self.pm.activatePluginByName(pluginInfo.name)
            logging.info("Plugin {0} activated".format(pluginInfo.name))

    def updateProgress(self, progress):
        '''Updates the Progress Bar.'''
        self.ui.progressBar.setValue(progress)

    def update_file_selected_text_field(self, route):
        ''''Sets self.image_file_route and ui.filename_lineedit to route.'''
        self.ui.filename_lineedit.setText(route)
        self.image_file_route = route

    def setupBehaviour(self):
        self.ui.load_file_button.clicked.connect(self.file_select_dialog)

    def file_select_dialog(self):
        file_selected = QtGui.QFileDialog.getOpenFileName(self)
        self.update_file_selected_text_field(file_selected)


class GenericThread(QtCore.QThread):
    '''A generic thread wrapper for functions on threads.'''

    def __init__(self, function, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        self.join()
        self.wait()

    def run(self):
        self.function(*self.args, **self.kwargs)
        return

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = GuiMain()
    window.show()
    sys.exit(app.exec_())
