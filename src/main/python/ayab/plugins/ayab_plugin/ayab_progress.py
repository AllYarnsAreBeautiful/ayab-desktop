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
#    Copyright 2014 Sebastian Oliva, Christian Obersteiner, Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

"""Knitting progress window"""

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from bitarray import bitarray
import numpy as np
from time import sleep


class Progress:

    def __init__(self):
        self.reset()

    def reset(self):
        self.current_row = 0
        self.total_rows = 0
        self.repeats = -1
        self.colorSymbol = ""
        self.hall_l = 0
        self.hall_r = 0
        self.carriage_type = ""
        self.carriage_position = 0
        self.lineNumber = 0
        self.color = 0
        self.alt_color = None
        self.bits = bitarray()

    def get_carriage_info(self, msg):
        hall_l = int((msg[2] << 8) + msg[3])
        hall_r = int((msg[4] << 8) + msg[5])

        if msg[6] == 1:
            carriage_type = "K Carriage"
        elif msg[6] == 2:
            carriage_type = "L Carriage"
        elif msg[6] == 3:
            carriage_type = "G Carriage"
        else:
            carriage_type = ""

        carriage_position = int(msg[7])

        self.hall_l = hall_l
        self.hall_r = hall_r
        self.carriage_type = carriage_type
        self.carriage_position = carriage_position


class KnitProgress:

    def __init__(self, parent):
        self.area = parent.area
        self.area.setContentsMargins(1, 1, 1, 1)
        self.container = QtWidgets.QWidget()
        self.container.setMinimumSize(100,100)
        self.grid = QtWidgets.QGridLayout(self.container)
        self.grid.setContentsMargins(1, 1, 1, 1)
        self.grid.setSpacing(0)
        self.grid.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.area.setWidget(self.container)
        self.row = -1

    def show(self):
        self.container.show()

    def hide(self):
        self.container.hide()

    def reset(self):
        self.row = -1

    def close(self):
        self.container.close()

    def update(self, progress, row_multiplier):
        if progress.lineNumber > self.row:
            self.row += 1
        if progress.lineNumber == self.row:
            row, swipe = divmod(progress.lineNumber, row_multiplier)
            if row < progress.total_rows or progress.repeats >= 0:
                # row header on new line
                direction = progress.lineNumber % 2
                w0 = label("Row")
                self.grid.addWidget(w0, progress.lineNumber, 0)
                w1 = label(str(row + 1))
                self.grid.addWidget(w1, progress.lineNumber, 1, 1, 1, Qt.AlignRight)
                w2 = label("Pass " + str(swipe + 1))
                self.grid.addWidget(w2, progress.lineNumber, 2)
                if progress.colorSymbol == "":
                    w3 = label("")
                else:
                    w3 = label("Color " + progress.colorSymbol)
                    self.grid.addWidget(w3, progress.lineNumber, 3)
                # TODO: report carriage
                # w4 = label("KR") # progress.carriage
                w4 = label(["\u2192 ","\u2190 "][direction])
                self.grid.addWidget(w4, progress.lineNumber, 4)
                # TODO: hints, notes, memos
                w0.show()
                w1.show()
                w2.show()
                w3.show()
                w4.show()
                self.area.ensureWidgetVisible(w0)
            # graph line of stitches
            for c in range(len(progress.bits)):
                wc = stitch(progress.color, progress.bits[c], progress.alt_color)
                self.grid.addWidget(wc, self.row, 6 + c)
            # if not infinite repeats, update progress bar
            # if progress.repeats < 0 and progress.total_rows > 0:  
            #     self.pd.setValue(100 * (row + 1) / progress.total_rows)
            # self.pd.update()
        return
        

def label(text):
    table = "<table><tbody><tr height='12'><td style='font-weight: normal;'>" + text + "</td></tr></tbody></table>"
    label = QtWidgets.QLabel()
    label.setText(table)
    label.setTextFormat(Qt.RichText)
    return label

def stitch(color, bit, alt_color=None, symbol=0x20):
    table = "<table style='font-weight: normal;'><tbody><tr height='12'><td width='12' align='center' "
    if bit:
        table = table + "style='border: 1 solid black; color: #{:06x}; background-color: #{:06x};'>".format(contrast_color(color), color) + chr(symbol)
    elif alt_color is not None:
        table = table + "style='border: 1 solid black; color: #{:06x}; background-color: #{:06x};'>".format(contrast_color(alt_color), alt_color) + chr(symbol)
    else:
        table = table + "style='border: 1 dotted black;'>"
    table = table + "</td></tr></tbody></table>"
    label = QtWidgets.QLabel()
    label.setText(table)
    label.setTextFormat(Qt.RichText)
    return label

def rgb2array(color):
    return np.array([color // 0x1000, (color // 0x100) & 0xFF, color & 0xFF])

def greyscale(rgb):
    return np.dot([.299, .587, .114], rgb)

def contrast_color(color):
    return [0x000000,0xFFFFFF][greyscale(rgb2array(color)) < 0x80]

