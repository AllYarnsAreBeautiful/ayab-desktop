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

from ayab_communication import AyabCommunication
import time
from plugins.knitting_plugin import KnittingPlugin
from PyQt4 import QtGui


class AyabPluginControl(KnittingPlugin):

  def onknit(self, e):
    #try:
        for i in range(self._cycle_ammount):
          print i
          self.__wait_for_user_action()
          time.sleep(1)
        return True
    #except:
        return False

  def onconfigure(self, e):
    assert e.parent_ui
    self.__parent_ui = e.parent_ui
    self._cycle_ammount = 3
    return

  def onfinish(self, e):
    pass

  def __wait_for_user_action(self):
    ret = QtGui.QMessageBox.warning(
        self.__parent_ui,
        "AYAB",
        "INIT MACHINE.\n",
        QtGui.QMessageBox.AcceptRole,
        QtGui.QMessageBox.AcceptRole)
    if ret == QtGui.QMessageBox.AcceptRole:
      return True

  def setup_ui(self, ui):
    pass

  def get_configuration_from_ui(self, ui):
    self.conf = {}
    start_line_text = ui.findChild(QtGui.QLineEdit, "start_line_edit").text()
    self.conf["start_line"] = int(start_line_text)
    start_needle_text = ui.findChild(QtGui.QLineEdit, "start_needle_edit").text()
    self.conf["start_needle"] = int(start_needle_text)
    stop_needle_text = ui.findChild(QtGui.QLineEdit, "stop_needle_edit").text()
    self.conf["stop_needle"] = int(stop_needle_text)
    alignment_text = ui.findChild(QtGui.QComboBox, "alignment_combo_box").currentText()
    self.conf["alignment"] = alignment_text
    machine_type_text = ui.findChild(QtGui.QComboBox, "machine_type_box").currentText()
    self.conf["machine_type"] = machine_type_text
    #TODO: add more config options
    return self.conf

  def __init__(self):
    callbacks_dict = {
        'onknit': self.onknit,
    }
    super(AyabPluginControl, self).__init__(callbacks_dict)
    # KnittingPlugin.__init__(self)
