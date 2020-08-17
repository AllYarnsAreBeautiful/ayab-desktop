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
from PyQt5.QtCore import pyqtSignal, Qt, QSize


class CmdLine(QPlainTextEdit):
    def __init__(self, parent):
        # set up UI
        super().__init__(parent)
        self.setCursor(Qt.IBeamCursor)
        self.ensureCursorVisible()
        # p = QPalette()
        # p.setColor(QPalette.Base, Qt.black)
        # p.setColor(QPalette.Text, Qt.green)
        # self.setPalette(p)
        self.setMaximumHeight(50)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.cmd_sender.connect(parent.send_cmd_API6)
        self.__hw_test_dialog = parent

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            # self.cmd_sender.emit("quit")
            self.__hw_test_dialog.send_cmd_API6("quit")
        elif key == Qt.Key_Return:
            # self.cmd_sender.emit(self.toPlainText())
            self.__hw_test_dialog.send_cmd_API6(self.toPlainText())
            self.setPlainText("")
        elif key == Qt.Key_Backspace:
            self.textCursor().deletePreviousChar()
        elif key in [
                Qt.Key_Delete, Qt.Key_Left, Qt.Key_Right, Qt.Key_Up,
                Qt.Key_Down
        ]:
            pass
        else:
            self.insertPlainText(event.text())

    def mousePressEvent(self, event):
        self.setFocus()

    def mouseDoubleClickEvent(self, event):
        pass

    def contextMenuEvent(self, event):
        pass
