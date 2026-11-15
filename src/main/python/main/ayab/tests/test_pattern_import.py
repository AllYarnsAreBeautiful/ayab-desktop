# -*- coding: utf-8 -*-
# This file is part of AYAB.
#
#    AYAB is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

from pathlib import Path
import unittest

from ..pattern_import import (
    CutPatternConverter,
    PatPatternConverter,
    StpPatternConverter,
)


DATA_DIR = Path(__file__).with_name("data")
EXPECTED_DAK_PIXELS = [
    (0, 0, 255),
    (0, 0, 255),
    (0, 0, 255),
    (255, 0, 0),
    (0, 0, 255),
    (255, 0, 0),
]


class TestPatternImport(unittest.TestCase):
    def test_designaknit_pat(self):
        image = PatPatternConverter(debug=False).pattern2im(
            str(DATA_DIR / "synthetic.pat")
        )

        assert image.mode == "RGB"
        assert image.size == (3, 2)
        assert list(image.getdata()) == EXPECTED_DAK_PIXELS

    def test_designaknit_stp(self):
        image = StpPatternConverter(debug=False).pattern2im(
            str(DATA_DIR / "synthetic.stp")
        )

        assert image.mode == "RGB"
        assert image.size == (3, 2)
        assert list(image.getdata()) == EXPECTED_DAK_PIXELS

    def test_dr_halo_cut(self):
        image = CutPatternConverter(debug=False).pattern2im(
            str(DATA_DIR / "synthetic.cut")
        )

        assert image.mode == "RGB"
        assert image.size == (3, 2)
        assert list(image.getdata()) == [
            (64, 64, 64),
            (64, 64, 64),
            (64, 64, 64),
            (0, 0, 0),
            (127, 127, 127),
            (255, 255, 255),
        ]
