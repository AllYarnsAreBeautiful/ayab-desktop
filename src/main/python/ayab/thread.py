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
from PySide6.QtCore import QThread
from typing import Callable, Any


class GenericThread(QThread):
    """A generic thread wrapper for functions on threads."""

    def __init__(self, function: Callable[..., Any], *args: Any, **kwargs: Any):
        QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self) -> None:
        self.wait()

    def run(self) -> None:
        try:
            self.function(*self.args, **self.kwargs)
        except Exception:
            for arg in self.args:
                print(arg)
            for key, value in self.kwargs.items():
                print(key, value)
            raise
