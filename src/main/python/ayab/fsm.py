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

import logging

from PyQt5.QtCore import QStateMachine, QState, QObject


class FSM(object):
    """Finite State Machine.

    This replaces `fsyom` and various imperatively-programmed structures
    with a declaratively-programmed, event-driven framework tailored to the UI.
    @author Tom Price
    @date   June 2020
    """
    def __init__(self):
        """Define Finite State Machine"""

        # Finite State Machine
        self.machine = QStateMachine()

        # Image states
        self.NO_IMAGE = QState(self.machine)
        self.CONFIGURING = QState(self.machine)
        self.CHECKING = QState(self.machine)
        self.KNITTING = QState(self.machine)
        # self.TESTING = QState(self.machine)

        # Set machine states
        self.machine.setInitialState(self.NO_IMAGE)

    def set_transitions(self, parent):
        """Define transitions between states for Finite State Machine"""

        # Events that trigger state changes
        self.NO_IMAGE.addTransition(parent.seer.got_image_flag,
                                    self.CONFIGURING)
        self.CONFIGURING.addTransition(parent.ui.knit_button.clicked,
                                       self.CHECKING)
        # self.CONFIGURING.addTransition(parent.ui.test_button.clicked,
        #                                self.TESTING)
        self.CHECKING.addTransition(parent.seer.got_image_flag,
                                    self.CONFIGURING)
        self.CHECKING.addTransition(parent.seer.new_image_flag,
                                    self.CONFIGURING)
        self.CHECKING.addTransition(parent.seer.bad_config_flag,
                                    self.CONFIGURING)
        self.CHECKING.addTransition(parent.seer.knitting_starter,
                                    self.KNITTING)
        self.KNITTING.addTransition(parent.engine_thread.finished,
                                    self.CONFIGURING)

        # Actions triggered by state changes
        self.NO_IMAGE.entered.connect(
            lambda: logging.debug("Entered state NO_IMAGE"))
        self.CONFIGURING.entered.connect(
            lambda: logging.debug("Entered state CONFIGURING"))
        self.CHECKING.entered.connect(
            lambda: logging.debug("Entered state CHECKING"))
        self.KNITTING.entered.connect(
            lambda: logging.debug("Entered state KNITTING"))
        # self.TESTING.entered.connect(
        #     lambda: logging.debug("Entered state TESTING"))

        self.NO_IMAGE.exited.connect(parent.engine.config.refresh)
        self.CONFIGURING.entered.connect(parent.menu.add_image_actions)
        self.CONFIGURING.entered.connect(parent.progbar.reset)
        self.CHECKING.entered.connect(
            lambda: parent.engine.knit_config(parent.scene.ayabimage.image))
        self.KNITTING.entered.connect(parent.start_knitting)

    def set_properties(self, parent):
        """
        Define properties for GUI elements linked to
        states in Finite State Machine
        """
        # Dock widget
        self.NO_IMAGE.assignProperty(parent.engine, "enabled", "False")
        self.CONFIGURING.assignProperty(parent.engine, "enabled", "True")
        self.KNITTING.assignProperty(parent.engine, "enabled", "False")
        # self.TESTING.assignProperty(parent.engine, "enabled", "False")

        # Status tab in options dock should be activated only when knitting
        # self.NO_IMAGE.assignProperty(ui.status_tab, "enabled", "False")
        # self.CONFIGURING.assignProperty(ui.status_tab, "enabled", "False")
        # self.KNITTING.assignProperty(ui.status_tab, "enabled", "True")
        # self.TESTING.assignProperty(ui.status_tab, "enabled", "False")  # ?

        # Knit button
        self.NO_IMAGE.assignProperty(parent.ui.knit_button, "enabled", "False")
        self.CONFIGURING.assignProperty(parent.ui.knit_button, "enabled", "True")
        self.KNITTING.assignProperty(parent.ui.knit_button, "enabled", "False")
        # self.TESTING.assignProperty(parent.ui.knit_button, "enabled", "False")

        # Test button
        # self.NO_IMAGE.assignProperty(parent.ui.test_button, "enabled", "True")
        # self.CONFIGURING.assignProperty(parent.ui.test_button, "enabled", "True")
        # self.KNITTING.assignProperty(parent.ui.knit_button, "enabled", "False")
        # self.TESTING.assignProperty(parent.ui.knit_button, "enabled", "False")

        # Cancel button
        self.NO_IMAGE.assignProperty(parent.ui.cancel_button, "enabled", "False")
        self.CONFIGURING.assignProperty(parent.ui.cancel_button, "enabled", "False")
        self.KNITTING.assignProperty(parent.ui.cancel_button, "enabled", "True")
        # self.TESTING.assignProperty(parent.ui.cancel_button, "enabled", "True")
