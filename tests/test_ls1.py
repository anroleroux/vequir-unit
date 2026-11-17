"""LS1, the single-cell unit: its base, lid and assembled model.

The holder comes from vequir-power, the boards, button and LED stick from
vequir-standard; ``libraries.txt`` expects both beside this repository.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cad.part import build_part

LS1 = Path(__file__).resolve().parents[1] / "products" / "LS1"


def _summary(result):
    assert result.ok, result.error
    return json.loads(result.files["summary"].read_text())


def test_the_ls1_base_has_its_usb_c_and_button_holes(tmp_path):
    base = _summary(build_part(LS1 / "base" / "part.py", tmp_path / "base"))
    assert base["bounding_box"]["size"][2] == pytest.approx(30.0)
    assert base["regions"]["usbc_hole"]["count"] == 4
    assert base["regions"]["button_hole"]["count"] == 1


def test_the_ls1_lid_has_a_window_for_each_led(tmp_path):
    lid = _summary(build_part(LS1 / "lid" / "part.py", tmp_path / "lid"))
    assert lid["regions"]["led_windows"]["count"] == 8 * 4  # four sides each


def test_the_ls1_assembly_places_everything_without_interference(tmp_path):
    summary = _summary(build_part(LS1 / "assembly.py", tmp_path / "out"))
    assert summary["interference"] == []
    names = {c["name"].split("/")[-1] for c in summary["components"]}
    assert names == {"base", "single_18650_holder", "mt3608_boost", "bms_1s_3a",
                     "usb_c_breakout", "tsd_1166_button", "ws2812_stick_8", "lid"}
    touching = {(c["a"].split("/")[-1], c["b"].split("/")[-1]) for c in summary["contacts"]}
    assert ("ws2812_stick_8", "lid") in touching  # the stick against the skirt
    assert ("base", "tsd_1166_button") in touching  # the button body against the back wall
