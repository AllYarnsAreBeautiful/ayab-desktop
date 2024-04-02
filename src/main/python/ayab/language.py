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

from __future__ import annotations
from os import path
from glob import glob
from PySide6.QtCore import QLocale
from PySide6.QtWidgets import QComboBox
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..main import AppContext


class Language(object):
    """
    Methods for selecting language and locale.

    @author Tom Price
    @date   July 2020
    """
    def __init__(self, app_context:AppContext):
        self.__app_context = app_context

    def add_items(self, box:QComboBox)->None:
        for loc in self.__available_locales():
            box.addItem(self.__native_language(loc), loc)

    def default_language(self)->str:
        default = self.__default_locale()
        available = self.__available_locales()
        if default in available:
            return default
        else:
            return "en_US"

    def __default_locale(self)->str:
        return QLocale.system().name()

    def __available_locales(self)->list[str]:
        lang_dir = self.__app_context.get_resource("ayab/translations")
        lang_files = glob(path.join(lang_dir, "ayab_trans.*.qm"))
        return sorted(map(self.__locale, lang_files))

    def __locale(self, string:str)->str:
        i = string.rindex("_")
        return string[i - 2:i + 3]

    def __native_language(self, loc:str)->str:
        lang = loc[0:3]
        country = loc[3:6]
        return QLocale(loc).nativeLanguageName()
        # return QLocale.languageToScript(QLocale(lang).language()) \
        # + " (" + country + ")"
