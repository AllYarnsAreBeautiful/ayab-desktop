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
from plugins.knitting_plugin import KnittingPlugin


class TestingKnittingPlugin(KnittingPlugin):

  def onknit(self, e):
    try:
        for i in range(e.many):
          print i
          time.sleep(1)
        return True
    except:
        return False

  def __init__(self):
    pass
    # callbacks_dict = {
    #     'onknit': self.onknit,
    # }
    # super(TestingKnittingPlugin, self).__init__(callbacks_dict)
    # KnittingPlugin.__init__(self)
