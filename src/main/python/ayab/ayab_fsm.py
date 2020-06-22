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
#    Copyright 2013-2020 Sebastian Oliva, Christian Obersteiner,
#    Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

import weakref
import logging

from PyQt5 import QtCore
from PyQt5.QtCore import QState, QObject

class FSM (object):
    """Heirarchical Finite State Machine.

    This replaces `fsyom` and various imperatively-programmed structures
    with a declaratively-programmed, event-driven framework tailored to the UI.
    @author Tom Price
    @date   June 2020
    """
    def __init__(self, parent):
        """Define Heirarchical states for Finite State Machine"""

        # garbage-collector-safe reference to parent
        self.__parent = parent  # weakref.ref(parent)

        # Finite State Machine
        self.machine = QtCore.QStateMachine()
 
        # Image states
        self.NO_IMAGE = QState()
        self.GOT_IMAGE = QState()
 
        # Set machine states
        self.machine.addState(self.NO_IMAGE)
        self.machine.addState(self.GOT_IMAGE)
        self.machine.setInitialState(self.NO_IMAGE)

        # Configuration states
        self.NOT_CONFIGURED = QState(self.GOT_IMAGE)
        self.CONFIGURING = QState(self.GOT_IMAGE)
        self.KNITTING = QState(self.GOT_IMAGE)
        self.GOT_IMAGE.setInitialState(self.NOT_CONFIGURED)

        # Knitting states
        self.OPERATING = QState(self.KNITTING)
        self.FINISHING = QState(self.KNITTING)
        self.KNITTING.setInitialState(self.OPERATING)

        # Pause states (not implemented)
        # self.NOT_PAUSED = QState(self.DO_TALK)
        # self.PAUSED = QState(self.DO_TALK)
        # self.DO_TALK.setInitialState(self.NOT_PAUSED)

        # Error states (not implemented)
        # self.ERROR_RAISED = QState()
        # self.ERROR_CLEARED = QState()

    def transitions(self):
        """Define transitions between states for Finite State Machine"""
 
        # Events that trigger state changes
        self.NO_IMAGE.addTransition(self.__parent.signalImageLoaded, self.GOT_IMAGE)
        self.NOT_CONFIGURED.addTransition(self.__parent.ui.knit_button.clicked, self.CONFIGURING)
        self.CONFIGURING.addTransition(self.__parent.signalImageLoaded, self.NOT_CONFIGURED)
        self.CONFIGURING.addTransition(self.__parent.signalImageTransformed, self.NOT_CONFIGURED)
        self.CONFIGURING.addTransition(self.__parent.signalConfigured, self.KNITTING)
        self.OPERATING.addTransition(self.__parent.ui.cancel_button.clicked, self.FINISHING)
        self.OPERATING.addTransition(self.__parent.signalDoneKnitProgress, self.FINISHING)
        self.FINISHING.addTransition(self.__parent.signalDoneKnitting, self.NOT_CONFIGURED)
 
        # self.UNPAUSED.addTransition(self.__parent.ui.pause_button.clicked, self.PAUSED)
        # self.PAUSED.addTransition(self.__parent.ui.pause_button.clicked, self.UNPAUSED)
 
        # self.ERROR_CLEARED.addTransition(..., self.ERROR_RAISED)
        # self.ERROR_RAISED.addTransition(..., self.ERROR_CLEARED)

        # Actions triggered by state changes
        self.NO_IMAGE.entered.connect(lambda: logging.debug("Entered state NO_IMAGE"))
        self.NOT_CONFIGURED.entered.connect(lambda: logging.debug("Entered state NOT_CONFIGURED"))
        self.CONFIGURING.entered.connect(lambda: logging.debug("Entered state CONFIGURING"))
        self.OPERATING.entered.connect(lambda: logging.debug("Entered state OPERATING"))
        self.FINISHING.entered.connect(lambda: logging.debug("Entered state FINISHING"))

        self.GOT_IMAGE.entered.connect(self.__parent.addImageActions)
        self.NOT_CONFIGURED.entered.connect(self.__parent.resetProgressBar)
        self.CONFIGURING.entered.connect(self.__parent.plugin.configure)
        self.KNITTING.entered.connect(self.__parent.start_knitting_process)
        self.FINISHING.entered.connect(self.__parent.plugin.finish)
        self.KNITTING.exited.connect(self.__parent.reset_ui_after_knitting)

    def properties(self):
        """Define properties for GUI elements linked to states in Finite State Machine"""

        # Knit button
        self.NO_IMAGE.assignProperty(self.__parent.ui.knit_button, "enabled", "False")
        self.NOT_CONFIGURED.assignProperty(self.__parent.ui.knit_button, "enabled", "True")
        self.KNITTING.assignProperty(self.__parent.ui.knit_button, "enabled", "False")

        # Cancel button
        self.NO_IMAGE.assignProperty(self.__parent.ui.cancel_button, "enabled", "False")
        self.NOT_CONFIGURED.assignProperty(self.__parent.ui.cancel_button, "enabled", "False")
        self.KNITTING.assignProperty(self.__parent.ui.cancel_button, "enabled", "True")

        # Pause button properties
        # self.NO_IMAGE.assignProperty(self.__parent.ui.pause_button, "enabled", "False")
        # self.NOT_CONFIGURED.assignProperty(self.__parent.ui.pause_button, "enabled", "False")
        # self.OPERATING.assignProperty(self.__parent.ui.pause_button, "enabled", "True")
        # self.CANCELING.assignProperty(self.__parent.ui.pause_button, "enabled", "False")
        # self.FINISHING.assignProperty(self.__parent.ui.pause_button, "enabled", "False")
        # self.UNPAUSED.assignProperty(self.__parent.ui.pause_button, "text", "Pause")
        # self.PAUSED.assignProperty(self.__parent.ui.pause_button, "text", "Resume")
        # self.ui.pause_button.clicked.connect(self.enabled_plugin.pause)
