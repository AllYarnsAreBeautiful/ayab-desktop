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
from time import sleep


class Ui_Progress:

    def __init__(self):
        self.pd = QtWidgets.QProgressDialog()
        self.pd.setMinimumSize(800, 400)
        self.pd.setModal(False)
        self.pd.setAutoClose(False)
        self.pd.setWindowTitle("Knitting Progress")
        ok_button = QtWidgets.QPushButton("Hide", self.pd)
        ok_button.clicked.connect(self.pd.accept)
        cancel_button = QtWidgets.QPushButton("Cancel", self.pd)
        cancel_button.clicked.connect(self.pd.reject)
        self.pd.setCancelButton(cancel_button)
        ok_button.clicked.connect(self.pd.accept)
        bar = QtWidgets.QProgressBar()
        self.pd.setBar(bar)
        group = QtWidgets.QGroupBox()
        group.setAlignment(Qt.AlignLeft)
        group.setFlat(True)
        group.setContentsMargins(3, 0, 3, 3)
        group.setMinimumSize(150, 100)
        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(1, 1, 1, 1)
        self.grid.setSpacing(0)
        self.grid.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        group.setLayout(self.grid)
        self.area = QtWidgets.QScrollArea()
        self.area.setWidget(group)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.area, 0, 0, 1, 14)
        layout.addWidget(ok_button, 1, 0)
        layout.addWidget(bar, 1, 2, 1, 10)
        layout.addWidget(cancel_button, 1, 13)
        self.pd.setLayout(layout)
        self.row = -1
        self.swipe = -1
        self.pd.show()

    def show(self):
        self.pd.show()

    def hide(self):
        self.pd.hide()

    def close(self):
        self.pd.done()
