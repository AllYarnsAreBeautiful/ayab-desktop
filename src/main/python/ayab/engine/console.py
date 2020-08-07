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

from PyQt5.QtWidgets import QPlainTextEdit, QScrollBar
from PyQt5.QtGui import QPalette, QTextCursor
from PyQt5.QtCore import pyqtSignal, Qt


class Console(QPlainTextEdit):
    data_getter = pyqtSignal(bytearray)

    def __init__(self, parent):
        super().__init__(parent)
        # self.bar = QScrollBar(self)
        # self.cursor = QTextCursor()
        self.setCursor(Qt.IBeamCursor)
        self.ensureCursorVisible()
        p = QPalette()
        p.setColor(QPalette.Base, Qt.black)
        p.setColor(QPalette.Text, Qt.green)
        self.setPalette(p)
        self.local_echo_enabled = True

    def put_data(self, data):
        self.insertPlainText(data)
        # self.bar.setValue(self.bar.maximum())

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()  # send signal to close parent dialog
            return
        # else
        if key in []:  #Qt.Key_Delete, Qt.Key_Backspace, Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down]:
            pass
        else:
            if self.local_echo_enabled:
                # QPlainTextEdit.keyPressEvent(event)
                self.put_data(event.text())
                # emit data_getter(event.text())

    def mousePressEvent(self, event):
        self.setFocus()

    def mouseDoubleClickEvent(self, event):
        pass

    def contextMenuEvent(self, event):
        pass
