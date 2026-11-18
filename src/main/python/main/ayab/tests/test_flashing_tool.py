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

from pathlib import Path
from unittest import mock

import pytest

from ..flashing_tool import (
    AvrDudeTool,
    BossacTool,
    FlashingError,
    FlashingToolFactory,
)


class FakeAppContext:
    def get_resource(self, path: str) -> str:
        return "/res/" + path


@pytest.fixture
def firmware(tmp_path: Path) -> str:
    path = tmp_path / "firmware.bin"
    path.write_bytes(b"\x00" * 16)
    return str(path)


def test_factory() -> None:
    assert isinstance(FlashingToolFactory.create_tool("uno"), AvrDudeTool)
    assert isinstance(FlashingToolFactory.create_tool("r4_wifi"), BossacTool)
    assert FlashingToolFactory.create_tool("unknown") is None


@pytest.mark.parametrize(
    "os_name,binary",
    [("Windows", "avrdude.exe"), ("Darwin", "avrdude_mac")],
)
def test_avrdude_bundled_command(os_name: str, binary: str, firmware: str) -> None:
    tool = AvrDudeTool(device="atmega328p", programmer="arduino")
    cmd = tool.generate_command(os_name, "PORT", firmware, FakeAppContext())
    assert cmd is not None
    assert cmd.startswith(f'"/res/ayab/firmware/{binary}" -p atmega328p')
    assert '-C "/res/ayab/firmware/avrdude.conf"' in cmd


def test_avrdude_linux_bundled(firmware: str) -> None:
    tool = AvrDudeTool(device="atmega328p", programmer="arduino")
    with mock.patch("platform.machine", return_value="x86_64"):
        cmd = tool.generate_command("Linux", "PORT", firmware, FakeAppContext())
    assert cmd is not None
    assert cmd.startswith('"/res/ayab/firmware/avrdude_linux"')
    assert '-C "/res/ayab/firmware/avrdude.conf"' in cmd


def test_avrdude_linux_other_arch_uses_path(firmware: str) -> None:
    tool = AvrDudeTool(device="atmega328p", programmer="arduino")
    with (
        mock.patch("platform.machine", return_value="aarch64"),
        mock.patch("shutil.which", return_value="/usr/bin/avrdude"),
    ):
        cmd = tool.generate_command("Linux", "PORT", firmware, FakeAppContext())
    assert cmd is not None
    assert cmd.startswith('"/usr/bin/avrdude"')
    assert "-C" not in cmd


def test_avrdude_linux_other_arch_missing(firmware: str) -> None:
    tool = AvrDudeTool(device="atmega328p", programmer="arduino")
    with (
        mock.patch("platform.machine", return_value="aarch64"),
        mock.patch("shutil.which", return_value=None),
    ):
        with pytest.raises(FlashingError):
            tool.flash("Linux", "PORT", firmware, FakeAppContext())


@pytest.mark.parametrize(
    "os_name,binary",
    [("Windows", "bossac.exe"), ("Darwin", "bossac_mac")],
)
def test_bossac_bundled_command(os_name: str, binary: str, firmware: str) -> None:
    cmd = BossacTool().generate_command(os_name, "PORT", firmware, FakeAppContext())
    assert cmd == (
        f'"/res/ayab/firmware/{binary}" --port="PORT" -U -e -w "{firmware}" -R'
    )


def test_bossac_linux(firmware: str) -> None:
    with mock.patch("platform.machine", return_value="x86_64"):
        cmd = BossacTool().generate_command("Linux", "P", firmware, FakeAppContext())
    assert cmd is not None
    assert cmd.startswith('"/res/ayab/firmware/bossac_linux"')
    with (
        mock.patch("platform.machine", return_value="aarch64"),
        mock.patch("shutil.which", return_value="/usr/bin/bossac"),
    ):
        cmd = BossacTool().generate_command("Linux", "P", firmware, FakeAppContext())
    assert cmd is not None
    assert cmd.startswith('"/usr/bin/bossac"')


def test_bossac_flash_touches_then_runs(firmware: str) -> None:
    tool = BossacTool(bootloader_delay=0)
    calls: list[str] = []
    with (
        mock.patch("serial.Serial") as serial_mock,
        mock.patch.object(tool, "_run", side_effect=lambda c: calls.append(c)),
    ):
        serial_mock.return_value.__enter__.side_effect = (
            lambda: calls.append("touch") or serial_mock.return_value
        )
        tool.flash("Darwin", "PORT", firmware, FakeAppContext())
    serial_mock.assert_called_once_with("PORT", 1200)
    assert calls[0] == "touch"
    assert calls[1].startswith('"/res/ayab/firmware/bossac_mac"')


def test_bossac_missing_firmware() -> None:
    with pytest.raises(FlashingError):
        BossacTool().flash("Darwin", "PORT", "/nonexistent.bin", FakeAppContext())


def test_bossac_bad_port_raises_flashing_error(firmware: str) -> None:
    with pytest.raises(FlashingError):
        BossacTool(bootloader_delay=0).flash(
            "Darwin", "/dev/nonexistent-ayab-port", firmware, FakeAppContext()
        )
