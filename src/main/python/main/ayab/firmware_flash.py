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
import re
from subprocess import run, STDOUT, PIPE, check_output

from .firmware_flash_gui import Ui_Firmware
from . import utils
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from .ayab import GuiMain

# press Esc to Quit dialog
# press Return to Flash firmware


class FirmwareFlash(QDialog):
    # Arduino devices and their `avrdude` names
    device_dict = {
        "uno": "atmega328p",
    }
    # Arduino programmers and their `avrdude` names
    programmer_dict = {
        "uno": "arduino",
    }

    port: str

    def __init__(self, parent: GuiMain):
        # TODO: add creator that does not depend from super to ease testing.
        super().__init__()
        self.__logger = logging.getLogger(type(self).__name__)
        self.__app_context = parent.app_context

        self.ui = Ui_Firmware()
        self.ui.setupUi(self) # type: ignore
        self.ui.flash_firmware.setEnabled(False)
        self.ui.flash_firmware.setDefault(True)
        self.load_json()

        self.ui.port_combo_box.currentIndexChanged.connect(self.port_selected)
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
        self.load_controllers()
        self.clean_firmware_list()

    def load_controllers(self) -> None:
        self.clean_controller_list()
        repo = self.json_object
        for controller in repo.get("controller", []):
            self.add_controller_to_list(controller)

    def controller_item_activated(self, control_qitem: QListWidgetItem) -> None:
        """
        Signal on controller_list activated.
        Triggers loading of firmwares.
        """
        self.load_firmware(control_qitem.text())
        self.ui.flash_firmware.setEnabled(False)

    def load_firmware(self, controller_qstring: str) -> None:
        self.clean_firmware_list()
        controller_key = str(controller_qstring)
        repo = self.json_object
        for firmware in repo["controller"][controller_key]:
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

    def add_controller_to_list(self, controller: QListWidgetItem) -> None:
        self.ui.controller_list.addItem(controller)

    def add_firmware_dict_to_list(self, firmware: dict[str, str]) -> None:
        # Could add more info to display, such as date.
        version = firmware.get("version", "unspecified version")
        self.ui.firmware_list.addItem(version)

    def execute_flash_command(self) -> bool:
        self.ui.flash_firmware.setEnabled(False)
        self.__logger.debug("port " + str(self.port))
        os_name = platform.system()
        base_dir = os.path.dirname(__file__)
        controller_name = str(self.ui.controller_list.currentItem().text())
        firmware_key = str(self.ui.firmware_list.currentItem().text())
        firmware_name = "firmware.hex"
        for firmware in self.json_object["controller"][controller_name]:
            if firmware.get("version") == firmware_key:
                firmware_name = firmware.get("file")

        if "eknitter" in controller_name:
            command = self.generate_command_eknitter(
                base_dir, os_name, controller_name, firmware_name
            )
        else:
            command = self.generate_command(
                base_dir, os_name, controller_name, firmware_name
            )

        if command is None:
            return False
        # else
        tr_ = QCoreApplication.translate
        try:
            check_output(command, stderr=STDOUT, timeout=10, shell=True)
        except Exception as e:
            self.__logger.info("Error flashing firmware: " + repr(e))
            utils.display_blocking_popup(
                tr_("Firmware", "Error flashing firmware."), "error"
            )
            return False
        else:
            self.__logger.info("Flashing done!")
            utils.display_blocking_popup(tr_("Firmware", "Flashing done!"))
            self.close()
            return True

    def generate_command_eknitter(
        self, base_dir: str, os_name: str, controller_name: str, firmware_name: str
    ) -> Optional[str]:
        if os_name == "Windows":
            exe_route = self.__app_context.get_resource("ayab/firmware/esp32/win64/esptool.exe")
            exe_route = "\"" + exe_route + "\""
        elif os_name == "Linux":
            exe_route = self.__app_context.get_resource("ayab/firmware/esp32/linux-amd64/esptool")
        elif os_name == "Darwin":  # macOS
            #exe_route = self.__parent_ui.app_context.get_resource("ayab/firmware/esp32/macos/esptool")
            exe_route = "esptool.py"
        
        binary_file = os.path.join(
            self.__app_context.get_resource("ayab/firmware"), firmware_name
        )

        if "fw" in firmware_name:
            exec_command = (
                f"{exe_route} -port {self.port} --baud 921600 --no-stub  write_flash"
                + f" --flash_size 8MB 0x10000 {binary_file} --force"
            )
        elif "fs" in firmware_name:
            exec_command = (
                f"{exe_route} -port {self.port} --baud 921600 --no-stub  write_flash"
                + f" --flash_size 8MB 0x670000 {binary_file} --force"
            )
        else:
            self.__logger.debug("error firmware or filesystem")
            return None

        self.__logger.debug(exec_command)
        return exec_command

    def generate_command(
        self, base_dir: str, os_name: str, controller_name: str, firmware_name: str
    ) -> Optional[str]:
        if os_name == "Windows":
            exe_route = self.__app_context.get_resource("ayab/firmware/avrdude.exe")
            exe_route = '"' + exe_route + '"'
        elif os_name == "Linux":
            # We assume avrdude is available in path
            try:
                # run subprocess
                result = run(["which", "avrdude"], stdout=PIPE, stderr=PIPE)
                print(result)
            except Exception:
                self.__logger.error("`avrdude` not found in path")
                utils.display_blocking_popup(
                    QCoreApplication.translate(
                        "FirmwareFlash", "Error flashing firmware: `avrdude` not found."
                    ),
                    "error",
                )
                return None
            exe_route = re.sub(r"\n$", r"", result.stdout.decode("ascii"))
        elif os_name == "Darwin":  # macOS
            exe_route = (
                '"' + self.__app_context.get_resource("ayab/firmware/avrdude_mac") + '"'
            )

        binary_file = os.path.join(
            self.__app_context.get_resource("ayab/firmware"), firmware_name
        )
        device = self.device_dict.get(controller_name)
        programmer = self.programmer_dict.get(controller_name, "wiring")

        # avrdude command.
        # http://www.ladyada.net/learn/avr/avrdude.html
        # http://sharats.me/the-ever-useful-and-neat-subprocess-module.html
        exec_command = (
            f"{exe_route} -p {device} -c {programmer} -P {self.port} -b115200"
            + f' -D -Uflash:w:"{binary_file}":i '
        )

        if os_name == "Windows":
            exec_command += (
                ' -C "'
                + self.__app_context.get_resource("ayab/firmware/avrdude.conf")
                + '"'
            )
        elif os_name == "Darwin":
            exec_command += (
                ' -C "'
                + self.__app_context.get_resource("ayab/firmware/avrdude_mac.conf")
                + '"'
            )

        self.__logger.debug(exec_command)
        return exec_command
