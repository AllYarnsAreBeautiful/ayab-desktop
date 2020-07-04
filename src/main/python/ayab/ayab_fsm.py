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
    """Heirarchical Finite State Machine.

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
        self.NOT_CONFIGURED = QState(self.machine)
        self.CONFIGURING = QState(self.machine)
        self.KNITTING = QState(self.machine)

        # Set machine states
        self.machine.setInitialState(self.NO_IMAGE)

    def set_transitions(self, parent):
        """Define transitions between states for Finite State Machine"""

        # Events that trigger state changes
        self.NO_IMAGE.addTransition(parent.mailbox.image_loaded_flagger,
                                    self.NOT_CONFIGURED)
        self.NOT_CONFIGURED.addTransition(parent.ui.knit_button.clicked,
                                          self.CONFIGURING)
        self.CONFIGURING.addTransition(parent.mailbox.image_loaded_flagger,
                                       self.NOT_CONFIGURED)
        self.CONFIGURING.addTransition(
            parent.mailbox.image_transformed_flagger, self.NOT_CONFIGURED)
        self.CONFIGURING.addTransition(
            parent.mailbox.configuration_fail_flagger, self.NOT_CONFIGURED)
        self.CONFIGURING.addTransition(parent.mailbox.configured_flagger,
                                       self.KNITTING)
        self.KNITTING.addTransition(parent.gt.finished, self.NOT_CONFIGURED)

        # Actions triggered by state changes
        self.NO_IMAGE.entered.connect(
            lambda: logging.debug("Entered state NO_IMAGE"))
        self.NOT_CONFIGURED.entered.connect(
            lambda: logging.debug("Entered state NOT_CONFIGURED"))
        self.CONFIGURING.entered.connect(
            lambda: logging.debug("Entered state CONFIGURING"))
        self.KNITTING.entered.connect(
            lambda: logging.debug("Entered state KNITTING"))

        self.NOT_CONFIGURED.entered.connect(parent.menu.add_image_actions)
        self.NOT_CONFIGURED.entered.connect(parent.pb.reset)
        self.CONFIGURING.entered.connect(
            lambda: parent.plugin.configure(parent.scene.image))
        self.KNITTING.entered.connect(parent.start_knitting_process)

    def set_properties(self, ui):
        """Define properties for GUI elements linked to states in Finite State Machine"""

        # Options dock
        self.NO_IMAGE.assignProperty(ui.widget_optionsdock, "enabled", "False")
        self.NOT_CONFIGURED.assignProperty(ui.widget_optionsdock, "enabled",
                                           "True")
        self.KNITTING.assignProperty(ui.widget_optionsdock, "enabled", "False")

        # Knit button
        self.NO_IMAGE.assignProperty(ui.knit_button, "enabled", "False")
        self.NOT_CONFIGURED.assignProperty(ui.knit_button, "enabled", "True")
        self.KNITTING.assignProperty(ui.knit_button, "enabled", "False")

        # Cancel button
        self.NO_IMAGE.assignProperty(ui.cancel_button, "enabled", "False")
        self.NOT_CONFIGURED.assignProperty(ui.cancel_button, "enabled",
                                           "False")
        self.KNITTING.assignProperty(ui.cancel_button, "enabled", "True")
