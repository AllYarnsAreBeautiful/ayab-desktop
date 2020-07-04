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


class Progress(object):
    """Data object for the progress bar."""
    def __init__(self):
        self.reset()

    def reset(self):
        self.row = -1
        self.total = -1
        self.repeats = -1
        self.color = ""


class ProgressBar(object):
    """Methods for the progress bar."""
    def __init__(self, parent):
        self.__progress = parent.progress
        self.__row_label = parent.ui.label_current_row
        self.__color_label = parent.ui.label_current_color
        self.__status_label = parent.plugin.ui.label_progress
        self.reset()

    def reset(self):
        self.__progress.reset()
        self.__row_label.setText("")
        self.__color_label.setText("")
        self.__status_label.setText("")
        self.refresh()

    def update(self, row, total=0, repeats=0, color_symbol=""):
        if row < 0:
            return
        self.__progress.row = row
        self.__progress.total = total
        self.__progress.repeats = repeats
        self.__progress.color = color_symbol
        self.refresh()

    def refresh(self):
        '''Updates the color and row in progress bar'''
        if self.__progress.row < 0 or self.__progress.total < 0:
            return

        if self.__progress.color == "":
            color_text = ""
        else:
            color_text = "Color " + self.__progress.color
        self.__color_label.setText(color_text)

        # Update labels
        if self.__progress.total == 0:
            row_text = ""
        else:
            row_text = "Row {0}/{1}".format(self.__progress.row,
                                            self.__progress.total)
            if self.__progress.repeats >= 0:
                row_text += " ({0} repeats completed)".format(
                    self.__progress.repeats)
        self.__row_label.setText(row_text)
        self.__status_label.setText("{0}/{1}".format(self.__progress.row,
                                                     self.__progress.total))
