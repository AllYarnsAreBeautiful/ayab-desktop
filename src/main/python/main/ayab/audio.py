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
"""Standalone audio player."""

from __future__ import annotations
from os import path

import simpleaudio as sa

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ayab import GuiMain


class AudioPlayer:
    def __init__(self, gui: GuiMain):
        self.__dir = gui.app_context.get_resource("assets")
        self.__prefs = gui.prefs
        self.__cache: dict[str, sa.WaveObject] = {}

    def play(self, sound: str) -> None:
        """Play audio."""
        if self.__prefs.value("quiet_mode"):
            return
        # else
        wave_obj = self.__wave(sound)
        if wave_obj is None:
            return
        # else
        wave_obj.play()

    def __wave(self, sound: str) -> sa.WaveObject | None:
        """Get and cache audio."""
        if sound not in self.__cache:
            wave_object = self.__load_wave(sound)
            if wave_object is None:
                return None
            self.__cache[sound] = wave_object
        return self.__cache[sound]

    def __load_wave(self, sound: str) -> sa.WaveObject | None:
        """Get audio from file."""
        filename = path.join(self.__dir, sound + ".wav")
        return sa.WaveObject.from_wave_file(filename)
