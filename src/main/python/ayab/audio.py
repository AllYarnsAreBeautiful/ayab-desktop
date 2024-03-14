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
"""Standalone audio player."""

from __future__ import annotations
import logging
from os import path

import simpleaudio as sa
import wave

from PySide6.QtCore import QObject, QThread
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .ayab import GuiMain

class AudioWorker(QObject):
    def __init__(self, parent:GuiMain):
        super().__init__()
        self.__dir = parent.app_context.get_resource("assets")
        self.__prefs = parent.prefs
        self.__cache:dict[str,sa.WaveObject] = {}

    def play(self, sound:str, blocking:bool=False)->None:
        """Play audio and wait until finished."""
        # thread remains open in quiet mode but sound does not play
        if self.__prefs.value("quiet_mode"):
            return
        # else
        wave_obj = self.__wave(sound)
        if wave_obj is None:
            return
        # else
        play_obj = wave_obj.play()
        if blocking:
            # wait until sound has finished before returning
            play_obj.wait_done()

    def __wave(self, sound:str)->Optional[sa.WaveObject]:
        """Get and cache audio."""
        if not sound in self.__cache:
            self.__cache[sound] = self.__load_wave(sound)
        return self.__cache[sound]

    def __load_wave(self, sound:str)->Optional[sa.WaveObject]:
        """Get audio from file."""
        filename = sound + ".wav"
        try:
            wave_read = wave.open(path.join(self.__dir, filename), 'rb')
        except FileNotFoundError:
            logging.warning("File " + filename + " not found.")
            return None
        except OSError:
            logging.warning("Error loading " + filename + ".")
            return None
        else:
            return sa.WaveObject.from_wave_read(wave_read)


class AudioPlayer(QThread):
    """Audio controller in its own thread."""
    def __init__(self, parent:GuiMain):
        super().__init__(parent)
        self.__worker = AudioWorker(parent)
        self.__worker.moveToThread(self)
        self.start()

    def __del__(self)->None:
        self.wait()

    def play(self, sound:str)->None:
        self.__worker.play(sound, blocking=False)
