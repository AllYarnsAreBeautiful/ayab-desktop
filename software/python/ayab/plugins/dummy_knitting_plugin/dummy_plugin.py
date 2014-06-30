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
from plugins.knitting_plugin import KnittingPlugin
import logging


class DummyKnittingPlugin(KnittingPlugin):

  def onknit(self, e):   # FIXME: setting options should go on onconfig.
    logging.debug("called onknit on DummyKnittingPlugin")
    for i in range(self._cycle_ammount):
      percent = (i / float(self._cycle_ammount))*100
      print percent
      self.parent_ui.emit(QtCore.SIGNAL('updateProgress(int)'), int(percent))
      time.sleep(0.1)
    self.finish()
    return True

  def onconfigure(self, e):
    logging.debug("called onconfigure on DummyKnittingPlugin")
    self.parent_ui = e.parent_ui
    self._cycle_ammount = 20
    return

  def onfinish(self, e):
    logging.info("finished knitting")
    pass

  def setup_ui(self, parent_ui):
    pass

  def cleanup_ui(self, parent_ui):
    pass

  def get_configuration_from_ui(self, ui):
    pass

  def __init__(self):
    super(DummyKnittingPlugin, self).__init__({})
    # callbacks_dict = {
    #     'onknit': self.onknit,
    # }
    # super(DummyKnittingPlugin, self).__init__(callbacks_dict)
    # KnittingPlugin.__init__(self)
