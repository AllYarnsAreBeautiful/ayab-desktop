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

from __future__ import annotations
import logging
from PIL import Image

from PySide6.QtCore import QCoreApplication, Signal, Slot
from PySide6.QtWidgets import QDockWidget
from wakepy import keep

from .. import utils
from ..machine import Machine
from .engine_fsm import Operation, State
from .pattern import Pattern
from .options import OptionsTab
from .status import Status, StatusTab
from .output import FeedbackHandler
from .dock_gui import Ui_Dock
from typing import TYPE_CHECKING, Literal, Optional, cast
from ..signal_sender import SignalSender

import ipaddress
from .mdns_discovery import MdnsBrowser

if TYPE_CHECKING:
    from ..ayab import GuiMain
from .control import Control


class Engine(SignalSender, QDockWidget):
    """
    Top-level class for the slave thread that communicates with the shield.

    Implemented as a subclass of `QDockWidget` and `SignalSender`.
    """

    port_opener = Signal()
    mdns_update_signal = Signal()

    pattern: Pattern
    status: StatusTab

    def __init__(self, parent: GuiMain):
        # set up UI
        super().__init__(parent.signal_receiver)
        self.mdns_browser = MdnsBrowser("_ayab._tcp.local.", self.mdns_update)
        self.mdns_update_signal.connect(self.__populate_ports)
        self.mdns_browser.start()

        self.ui = Ui_Dock()
        self.ui.setupUi(self)
        self.config: OptionsTab = OptionsTab(parent)
        self.config.portname = self.__read_portname()
        self.reload_settings()
        self.status = StatusTab()
        self.setup_ui()
        parent.ui.dock_container_layout.addWidget(self)

        self.pattern: Pattern = None  # type:ignore
        self.control = Control(parent, self)
        self.__feedback = FeedbackHandler(parent)
        self.__logger = logging.getLogger(type(self).__name__)

    def __del__(self) -> None:
        self.control.stop()
        self.mdns_browser.stop() # Lead to EventLoopBlocked exception when closing the window rather than the application

    @Slot()
    def mdns_update(self) -> None:
        """
        This method can be called from a non-Qt thread
        """
        self.mdns_update_signal.emit()

    def setup_ui(self) -> None:
        # insert tabs
        tr_ = QCoreApplication.translate
        self.ui.tab_widget.insertTab(0, self.config, tr_("Dock", "Settings"))
        self.ui.tab_widget.insertTab(1, self.status, tr_("Dock", "Status"))

        # disable status tab at first
        self.__disable_status_tab()

        # remove Status tab for now
        self.__close_status_tab()

        # activate UI elements
        self.__activate_ui()

    def reload_settings(self) -> None:
        self.config.refresh()
        self.setWindowTitle(
            QCoreApplication.translate("Dock", "Machine")
            + ": "
            + Machine(self.config.machine).name
        )

    def __disable_status_tab(self) -> None:
        self.ui.tab_widget.setTabEnabled(1, False)
        self.status.ui.label_progress.setText("")
        self.status.ui.label_direction.setText("")
        self.status.active = False

    def __close_status_tab(self) -> None:
        self.ui.tab_widget.removeTab(1)
        self.status.active = False

    def __activate_ui(self) -> None:
        """Connects UI elements to signal slots."""
        self.__populate_ports()
        self.ui.refresh_ports_button.clicked.connect(self.__populate_ports)

    def __populate_ports(self, port_list: Optional[list[str]] = None) -> None:
        combo_box = self.ui.serial_port_dropdown
        utils.populate_ports(combo_box, port_list)
        # Add Simulation item to indicate operation without machine
        combo_box.addItem(QCoreApplication.translate("KnitEngine", "Simulation"))

        # When starting up, mdns services won't be available yet, i.e. refresh button required
        # => Shouldn't this list be updated in background ?
        for _key, value in self.mdns_browser.get_known_services().items():
            if value and value.server:
                server_name = value.server.removesuffix('.local.')
                try:
                    server_ip = str(ipaddress.IPv4Address(value.addresses[0]))
                except ipaddress.AddressValueError:
                    server_ip = 'unknown'
                combo_box.addItem(f"{server_name} ({server_ip})", value)

    def __read_portname(self) -> str:
        # FIXME: method should return a class rather than a string to forward additional data
        selected_index = self.ui.serial_port_dropdown.currentIndex()
        user_data = self.ui.serial_port_dropdown.itemData(selected_index)
        if user_data:
            # Websocket connection
            portname = f"ws://{user_data.server}:{user_data.port}/ws"
            self.__logger.info(f"Connecting to {portname} ({user_data.properties[b'board_id'].decode()})")
        else:
            # Serial connection (default)
            portname = self.ui.serial_port_dropdown.currentText()
        return portname

    def knit_config(self, image: Image.Image) -> None:
        """
        Read and check configuration options from options dock UI.
        """
        # get configuration options
        self.config.read(self.__read_portname())
        self.__logger.debug(self.config.as_dict())

        # start to knit with the bottom first
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

        # TODO: detect if previous conf had the same
        # image to avoid re-generating.
        self.pattern = Pattern(image, self.config, self.config.num_colors)

        # validate configuration options
        valid, msg = self.validate()
        if not valid:
            self.emit_popup(cast(str, msg))
            self.emit_bad_config_flag()

        # update pattern
        self.pattern.set_knit_needles(
            self.config.start_needle, self.config.stop_needle, self.config.machine
        )
        self.pattern.alignment = self.config.alignment

        # update progress bar
        data = Status()
        data.copy(self.status)
        self.emit_progress_bar_updater(data)

        # switch to status tab
        # if self.config.continuous_reporting:
        #     self.__status_tab.activate()

        # send signal to start knitting
        self.emit_knitting_starter()

    def validate(self) -> tuple[Literal[False], str] | tuple[Literal[True], None]:
        if self.config.start_row > self.pattern.pat_height:
            return False, "Start row is larger than the image."
        # else
        return self.config.validate()

    def run(self, operation: Operation) -> None:
        self.__canceled = False

        # setup knitting controller
        self.config.portname = self.__read_portname()
        self.control.start(self.pattern, self.config, operation)

        with keep.presenting(on_fail="pass"):
            while True:
                # continue operating
                # typically each step involves some communication with the device
                output = self.control.operate(operation)
                if output != self.control.notification:
                    self.__feedback.handle(output)
                    self.control.notification = output
                if operation == Operation.KNIT:
                    self.__handle_status()
                if self.__canceled or self.control.state == State.FINISHED:
                    break

            self.control.stop()

            if operation == Operation.KNIT:
                if self.__canceled:
                    self.emit_notification("Knitting canceled.")
                    self.__logger.info("Knitting canceled.")
                else:
                    # operation == Operation.TEST:
                    self.__logger.info("Finished knitting.")
            else:
                # TODO: provide translations for these messages
                self.__logger.info("Finished testing.")

            # send signal to finish operation
            self.emit_operation_finisher(operation)

    def __handle_status(self) -> None:
        if self.status.active:
            self.status.refresh()
        # If we do not make a copy of status object to emit to the UI thread
        # then the signal knit_progress_updater must use a blocking connection
        # that holds up this thread until the knit progress window has finished
        # updating, Otherwise if the knit progress window lags the status
        # will change before the information is written to the UI.
        status_copy = Status()
        status_copy.copy(self.status)
        self.emit_knit_progress_updater(status_copy)
        self.emit_progress_bar_updater(status_copy)

    def cancel(self) -> None:
        self.__canceled = True
