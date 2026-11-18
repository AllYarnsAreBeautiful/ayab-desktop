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
#    Copyright 2014 Sebastian Oliva, Christian Obersteiner,
#       Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

from __future__ import annotations
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QDialog, QListWidget, QListWidgetItem

import json
import logging
import os
import platform

from .firmware_flash_gui import Ui_Firmware
from .flashing_tool import FlashingError, FlashingToolFactory
from . import utils
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .ayab import GuiMain

# press Esc to Quit dialog
# press Return to Flash firmware


class FirmwareFlash(QDialog):
    port: str
    machine_type: str = ""

    # User-friendly names for machines
    machine_display_names = {
        "brother": "Brother",
        "silverreed": "Silverreed",
    }

    # User-friendly names for controllers
    controller_display_names = {
        "uno": "Arduino Uno R3",
        "r4_wifi": "Arduino Uno R4 WiFi",
    }

    def __init__(self, parent: GuiMain):
        # TODO: add creator that does not depend from super to ease testing.
        super().__init__()
        self.__logger = logging.getLogger(type(self).__name__)
        self.__app_context = parent.app_context

        self.ui = Ui_Firmware()
        self.ui.setupUi(self)
        self.ui.flash_firmware.setEnabled(False)
        self.ui.flash_firmware.setDefault(True)
        self.load_json()

        self.ui.port_combo_box.currentIndexChanged.connect(self.port_selected)
        self.ui.machine_combo_box.currentIndexChanged.connect(self.machine_selected)
        self.ui.controller_list.itemClicked.connect(self.controller_item_activated)
        self.ui.firmware_list.itemClicked.connect(self.firmware_item_activated)
        self.ui.flash_firmware.clicked.connect(self.execute_flash_command)

    def open(self) -> None:
        utils.populate_ports(self.ui.port_combo_box)
        self.port_selected()
        self.show()

    def close(self) -> bool:
        """Close dialog and clean firmware list."""
        # self.clean_controller_list()
        self.clean_firmware_list()
        self.accept()
        return True

    def load_json(self) -> None:
        self.json_object = self.parse_json("")
        self.add_items_from_json_object()

    def parse_json(self, json_string: str) -> Any:  # TODO: type me tighter!
        path = self.__app_context.get_resource("ayab/firmware/firmware.json")
        with open(path) as data_file:
            data = json.load(data_file)
        return data

    def add_items_from_json_object(self) -> None:
        self.load_machines()
        self.clean_controller_list()
        self.clean_firmware_list()

    def load_machines(self) -> None:
        self.ui.machine_combo_box.clear()
        repo = self.json_object
        machine_types = repo.get("machine_type", {})
        for machine_key in machine_types:
            display_name = self.machine_display_names.get(machine_key, machine_key)
            self.ui.machine_combo_box.addItem(display_name, machine_key)

    def machine_selected(self) -> None:
        """Signal on machine_combo_box index changed.

        Triggers loading of controllers.
        """
        machine_key = self.ui.machine_combo_box.currentData()
        self.machine_type = machine_key
        self.clean_controller_list()
        if machine_key:
            self.load_controllers(str(machine_key))
        self.clean_firmware_list()
        self.ui.flash_firmware.setEnabled(False)

    def load_controllers(self, machine_type: str) -> None:
        repo = self.json_object
        machine_types = repo.get("machine_type", {})
        controllers = machine_types.get(machine_type, {}).get("controllers", {})
        for controller_key in controllers:
            self.add_controller_to_list(controller_key)

    def controller_item_activated(self, control_qitem: QListWidgetItem) -> None:
        """
        Signal on controller_list activated.
        Triggers loading of firmwares.
        """
        controller_key = control_qitem.data(32)  # Get controller key from user role
        self.load_firmware(self.machine_type, controller_key)
        self.ui.flash_firmware.setEnabled(False)

    def load_firmware(self, machine_type: str, controller_key: str) -> None:
        self.clean_firmware_list()
        repo = self.json_object
        machine_types = repo.get("machine_type", {})
        controllers = machine_types.get(machine_type, {}).get("controllers", {})
        firmwares = controllers.get(controller_key, [])
        for firmware in firmwares:
            self.add_firmware_dict_to_list(firmware)

    def firmware_item_activated(self, firmware_qitem: QListWidgetItem) -> None:
        """Signal on firmware_list activated."""
        self.ui.flash_firmware.setEnabled(self.valid_port())

    def valid_port(self) -> bool:
        return self.port != ""

    def port_selected(self) -> None:
        self.port = self.ui.port_combo_box.currentText()

    def clean_controller_list(self) -> None:
        self.__clean_QListWidget(self.ui.controller_list)

    def clean_firmware_list(self) -> None:
        self.__clean_QListWidget(self.ui.firmware_list)

    def __clean_QListWidget(self, qlistw: QListWidget) -> None:
        qlistw.clear()

    def add_controller_to_list(self, controller_key: str) -> None:
        display_name = self.controller_display_names.get(controller_key, controller_key)
        item = QListWidgetItem(display_name)
        item.setData(32, controller_key)  # Store controller key in user role
        self.ui.controller_list.addItem(item)

    def add_firmware_dict_to_list(self, firmware: dict[str, str]) -> None:
        # Could add more info to display, such as date.
        version = firmware.get("version", "unspecified version")
        self.ui.firmware_list.addItem(version)

    def execute_flash_command(self) -> bool:
        self.ui.flash_firmware.setEnabled(False)
        self.__logger.debug("port " + str(self.port))
        os_name = platform.system()

        # Get selected machine and controller
        machine_key = self.ui.machine_combo_box.currentData()
        if not machine_key:
            utils.display_blocking_popup(
                QCoreApplication.translate("Firmware", "Please select a machine type."),
                "error",
            )
            self.ui.flash_firmware.setEnabled(True)
            return False

        machine_type = str(machine_key)
        controller_item = self.ui.controller_list.currentItem()
        controller_name = controller_item.data(32)  # Get controller key from user role
        firmware_key = str(self.ui.firmware_list.currentItem().text())

        # Find the firmware file for this machine, controller, and version
        firmware_name = "firmware.hex"
        machine_types = self.json_object.get("machine_type", {})
        controllers = machine_types.get(machine_type, {}).get("controllers", {})
        firmwares = controllers.get(controller_name, [])
        for firmware in firmwares:
            if firmware.get("version") == firmware_key:
                firmware_name = firmware.get("file")
                break

        if not self._flash(os_name, controller_name, firmware_name):
            self.ui.flash_firmware.setEnabled(True)
            return False
        self.__logger.info("Flashing done!")
        utils.display_blocking_popup(
            QCoreApplication.translate("Firmware", "Flashing done!")
        )
        self.close()
        return True

    def _flash(self, os_name: str, controller_name: str, firmware_name: str) -> bool:
        """Flash the firmware with the tool matching the controller."""
        tool = FlashingToolFactory.create_tool(controller_name)
        if tool is None:
            self.__logger.error("Unknown controller: %s", controller_name)
            utils.display_blocking_popup(
                QCoreApplication.translate(
                    "Firmware",
                    f"Error: Unknown controller '{controller_name}'.",
                ),
                "error",
            )
            return False

        firmware_path = os.path.join(
            self.__app_context.get_resource("ayab/firmware"), firmware_name
        )

        if not tool.verify_firmware_path(firmware_path):
            self.__logger.error("Firmware file not found or empty: %s", firmware_path)
            utils.display_blocking_popup(
                QCoreApplication.translate(
                    "Firmware",
                    "Error flashing firmware: firmware file not found or empty.",
                ),
                "error",
            )
            return False

        try:
            tool.flash(os_name, self.port, firmware_path, self.__app_context)
        except FlashingError as e:
            self.__logger.error("Error flashing firmware: %s", e)
            utils.display_blocking_popup(
                QCoreApplication.translate(
                    "Firmware",
                    "Error flashing firmware. Check the AYAB log for details.",
                ),
                "error",
            )
            return False
        return True
