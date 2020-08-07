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
#    Copyright 2013 Christian Obersteiner, Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop
import serial

from .test_mock import TestMock
from .communication import Communication
from .communication_mockup import CommunicationMockup
from ayab import GenericThread

if portname == Simulation:
    self.__com = CommunicationMockup()
    self.test_mock = TestMock()
    self.test_mock_thread = GenericThread(self.test_mock.loop)
    self.test_mock_thread.start()

# test mock thread goes on forever unless it is killed
