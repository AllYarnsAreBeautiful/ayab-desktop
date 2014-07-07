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
#    Copyright 2013, 2014 Sebastian Oliva, Christian Obersteiner, Andreas Müller
#    https://bitbucket.org/chris007de/ayab-apparat/

import time
from PyQt4 import QtGui, QtCore
from ayab.plugins.knitting_plugin import KnittingPlugin
import logging

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


class DummyKnittingPlugin(KnittingPlugin):

  def onknit(self, e):
    logging.debug("called onknit on DummyKnittingPlugin")
    # Simulating a blocking task.
    for i in range(self._cycle_ammount):
      percent = (i / float(self._cycle_ammount))*100
      print percent
      self.parent_ui.emit(QtCore.SIGNAL('updateProgress(int)'), int(percent))
      time.sleep(0.1)
    self.finish()
    return True

  def onconfigure(self, e):
    logging.debug("Called onconfigure on DummyKnittingPlugin")
    self._cycle_ammount = 20
    return

  def onfinish(self, e):
    logging.info("Finished Knitting")
    pass

  def setup_ui(self, parent_ui):
    self.parent_ui = parent_ui
    dock = parent_ui.ui.knitting_options_dock
    self.qwidget = QtGui.QWidget(dock)
    self.configure_button = QtGui.QPushButton(self.qwidget)
    self.configure_button.setObjectName(_fromUtf8("configure_button"))
    self.configure_button.setText(_translate("DockWidget", "Configure", None))
    self.configure_button.clicked.connect(self.__conf_button_function)
    dock.setWidget(self.qwidget)

  def cleanup_ui(self, parent_ui):
    self.parent_ui = parent_ui
    dock = parent_ui.ui.knitting_options_dock
    cleaner = QtCore.QObjectCleanupHandler()
    cleaner.add(self.qwidget)
    self.__qw = QtGui.QWidget()
    dock.setWidget(self.__qw)

  def __conf_button_function(self):
    self.configure()

  def get_configuration_from_ui(self, ui):
    pass

  def __init__(self):
    super(DummyKnittingPlugin, self).__init__({})
