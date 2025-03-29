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

from enum import Enum

from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QWidget, QComboBox
from PySide6.QtGui import QPixmap

from ..signal_sender import SignalSender
from .options_gui import Ui_Options
from .mode import Mode
from ..machine import Machine
from . import lowercase_e_rc
from . import lowercase_e_reversed_rc
from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from ..ayab import GuiMain

OptionsTabDict = TypedDict(
    "OptionsTabDict",
    {
        "portname": str,
        "machine": str,
        "mode": str,
        "num_colors": int,
        "start_row": int,
        "inf_repeat": bool,
        "start_needle": int,
        "stop_needle": int,
        "alignment": str,
        "auto_mirror": bool,
        "continuous_reporting": bool,
    },
)


# FIXME translations for UI
class OptionsTab(SignalSender, QWidget):
    """
    Class for the configuration options tab of the dock widget,
    implemented as a subclass of `QWidget`.

    @author Tom Price
    @date   June 2020
    """

    lowercase_e_rc
    lowercase_e_reversed_rc
    alignment: Alignment
    auto_mirror: bool
    continuous_reporting: bool
    inf_repeat: bool
    machine: Machine
    mode: Mode
    num_colors: int
    portname: str
    start_needle: int
    start_row: int
    stop_needle: int

    def __init__(self, parent: GuiMain):
        super().__init__(parent.signal_receiver)
        self.prefs = parent.prefs
        self.auto_mirror = False
        self.ui = Ui_Options()
        self.__setup_ui()
        self.__activate_ui()
        # self.__reset()

    def __setup_ui(self) -> None:
        self.ui.setupUi(self)

        # Combo boxes
        Mode.add_items(self.ui.knitting_mode_box)
        Alignment.add_items(self.ui.alignment_combo_box)
        NeedleColor.add_items(self.ui.start_needle_color)
        NeedleColor.add_items(self.ui.stop_needle_color)
        self.ui.start_needle_color.setCurrentIndex(0)  # orange
        self.ui.stop_needle_color.setCurrentIndex(1)  # green

        # Remove "continuous reporting" checkbox tab for now
        self.ui.continuous_reporting_checkbox.setVisible(False)

    def __activate_ui(self) -> None:
        """Connects UI elements to signal slots."""
        self.ui.start_row_edit.valueChanged.connect(
            lambda: self.emit_start_row_updater(self.__read_start_row())
        )
        self.ui.start_needle_edit.valueChanged.connect(self.update_needles)
        self.ui.stop_needle_edit.valueChanged.connect(self.update_needles)
        self.ui.start_needle_color.currentIndexChanged.connect(self.update_needles)
        self.ui.stop_needle_color.currentIndexChanged.connect(self.update_needles)
        self.ui.alignment_combo_box.currentIndexChanged.connect(
            lambda: self.emit_alignment_updater(self.__read_alignment())
        )
        self.ui.auto_mirror_checkbox.clicked.connect(self.__auto_mirror_changed)

    def update_needles(self) -> None:
        """Sends the needles_updater signal."""
        self.__update_machine()
        start_needle = NeedleColor.read_start_needle(self.ui, self.machine)
        stop_needle = NeedleColor.read_stop_needle(self.ui, self.machine)
        self.emit_needles_updater(start_needle, stop_needle)

    def __auto_mirror_changed(self) -> None:
        image_reversed = self.ui.auto_mirror_checkbox.isChecked()
        if image_reversed:
            self.ui.auto_mirror_icon.setPixmap(QPixmap(":/garamond-lowercase-e.png"))
        else:
            self.ui.auto_mirror_icon.setPixmap(
                QPixmap(":/garamond-lowercase-e-reversed.png")
            )
        self.emit_image_reverser(image_reversed)

    def __read_start_row(self) -> int:
        return int(self.ui.start_row_edit.value()) - 1

    def __read_alignment(self) -> Alignment:
        return Alignment(self.ui.alignment_combo_box.currentIndex())

    def __update_machine(self) -> None:
        self.machine = Machine(self.prefs.value("machine"))
        self.ui.start_needle_edit.setMaximum(self.machine.width // 2)
        self.ui.stop_needle_edit.setMaximum(self.machine.width // 2)

    def __reset(self) -> None:
        """Reset configuration options to default settings."""
        self.__update_machine()
        self.mode = Mode(self.prefs.value("default_knitting_mode"))
        self.num_colors = 2
        self.start_row = 0
        self.inf_repeat = self.prefs.value("default_infinite_repeat")
        self.start_needle = 0
        self.stop_needle = self.machine.width
        self.alignment = Alignment(self.prefs.value("default_alignment"))
        self.auto_mirror = self.prefs.value("default_knit_side_image")
        self.continuous_reporting = False

    def refresh(self) -> None:
        """
        Refresh tab to default configuration options.
        This is called when the dock is activated after
        loading an image, in case the defaults have changed.
        There is no need to refresh options that do not have
        default settings.
        """
        self.__reset()
        self.ui.knitting_mode_box.setCurrentIndex(self.mode.value)
        # self.ui.color_edit
        # self.ui.start_row_edit
        if self.inf_repeat:
            self.ui.inf_repeat_checkbox.setCheckState(Qt.CheckState.Checked)
        else:
            self.ui.inf_repeat_checkbox.setCheckState(Qt.CheckState.Unchecked)
        # self.ui.start_needle_color
        # self.ui.start_needle_edit
        # self.ui.stop_needle_color
        # self.ui.stop_needle_edit
        self.ui.alignment_combo_box.setCurrentIndex(self.alignment.value)
        if self.auto_mirror:
            self.ui.auto_mirror_checkbox.setCheckState(Qt.CheckState.Checked)
            self.ui.auto_mirror_icon.setPixmap(QPixmap(":/garamond-lowercase-e.png"))
        else:
            self.ui.auto_mirror_checkbox.setCheckState(Qt.CheckState.Unchecked)
            self.ui.auto_mirror_icon.setPixmap(
                QPixmap(":/garamond-lowercase-e-reversed.png")
            )
        # self.ui.continuous_reporting_checkbox
        self.emit_image_reverser(self.auto_mirror)

    def as_dict(self) -> OptionsTabDict:
        return OptionsTabDict(
            {
                "portname": self.portname,
                "machine": self.machine.name,
                "mode": self.mode.name,
                "num_colors": self.num_colors,
                "start_row": self.start_row,
                "inf_repeat": self.inf_repeat,
                "start_needle": self.start_needle,
                "stop_needle": self.stop_needle,
                "alignment": self.alignment.name,
                "auto_mirror": self.auto_mirror,
                "continuous_reporting": self.continuous_reporting,
            }
        )

    def read(self, portname: str) -> None:
        """Get configuration options from the UI elements."""
        self.__update_machine()
        self.portname = portname
        self.mode = Mode(self.ui.knitting_mode_box.currentIndex())
        self.num_colors = int(self.ui.color_edit.value())
        self.start_row = self.__read_start_row()
        self.inf_repeat = self.ui.inf_repeat_checkbox.isChecked()
        self.start_needle = NeedleColor.read_start_needle(self.ui, self.machine)
        self.stop_needle = NeedleColor.read_stop_needle(self.ui, self.machine)
        self.alignment = self.__read_alignment()
        self.auto_mirror = self.ui.auto_mirror_checkbox.isChecked()
        # self.continuous_reporting =
        #     self.ui.continuous_reporting_checkbox.isChecked()

    def set_image_dimensions(self, width: int, height: int) -> None:
        """
        Called by Main UI on loading or transformation of an image
        to set start and stop needles to image width.
        Updates the maximum value of the Start Row UI element.
        """
        left_side = width // 2
        self.ui.start_needle_color.setCurrentIndex(0)  # orange
        self.ui.start_needle_edit.setValue(left_side)
        self.ui.stop_needle_color.setCurrentIndex(1)  # green
        self.ui.stop_needle_edit.setValue(width - left_side)
        self.ui.start_row_edit.setMaximum(height)

    def validate(self) -> tuple[Literal[False], str] | tuple[Literal[True], None]:
        """Validate configuration options."""
        if self.portname == "":
            return False, "Please choose a valid port."
        # else
        if self.start_needle and self.stop_needle:
            if self.start_needle > self.stop_needle:
                return False, "Invalid needle start and end."
        # else
        if self.mode == Mode.SINGLEBED and self.num_colors >= 3:
            return False, "Single bed knitting currently supports only 2 colors."
        # else
        if self.mode == Mode.CIRCULAR_RIBBER and self.num_colors >= 3:
            return False, "Circular knitting supports only 2 colors."
        # else
        return True, None


class Alignment(Enum):
    CENTER = 0
    LEFT = 1
    RIGHT = 2

    @staticmethod
    def add_items(box: QComboBox) -> None:
        """Add items to alignment combo box."""
        tr_ = QCoreApplication.translate
        box.addItem(tr_("Alignment", "Center"))
        box.addItem(tr_("Alignment", "Left"))
        box.addItem(tr_("Alignment", "Right"))


class NeedleColor(Enum):
    ORANGE = 0
    GREEN = 1

    @staticmethod
    def add_items(box: QComboBox) -> None:
        """Add items to needle color combo box."""
        tr_ = QCoreApplication.translate
        box.addItem(tr_("NeedleColor", "left"))
        box.addItem(tr_("NeedleColor", "right"))

    def read(self, needle: int, machine: Machine) -> int:
        if self == NeedleColor.ORANGE:
            return machine.width // 2 - int(needle)
        elif self == NeedleColor.GREEN:
            return machine.width // 2 + int(needle) - 1

    @staticmethod
    def read_start_needle(ui: Ui_Options, machine: Machine) -> int:
        """Read the start needle prefs from UI and normalize"""
        start_needle_col = NeedleColor(ui.start_needle_color.currentIndex())
        start_needle_text = ui.start_needle_edit.value()
        return start_needle_col.read(start_needle_text, machine)

    @staticmethod
    def read_stop_needle(ui: Ui_Options, machine: Machine) -> int:
        """Read the stop needle prefs from UI and normalize"""
        stop_needle_col = NeedleColor(ui.stop_needle_color.currentIndex())
        stop_needle_text = ui.stop_needle_edit.value()
        return stop_needle_col.read(stop_needle_text, machine)
