"""LS1, the single-cell unit: its base, lid and assembled model.

The holder comes from vequir-power, the boards, button, buzzer, sensor,
LED stick and screws from
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
    assert base["regions"]["pico_tap_holes"]["count"] == 4  # the Pico's four posts
    assert base["regions"]["mt_slots"]["count"] == 2  # the MT3608's two slotted posts


def test_the_ls1_lid_has_a_window_for_each_led(tmp_path):
    lid = _summary(build_part(LS1 / "lid" / "part.py", tmp_path / "lid"))
    assert lid["regions"]["led_windows"]["count"] == 8 * 4  # four sides each
    assert lid["regions"]["stick_pillars"]["count"] == 2
    assert lid["regions"]["tap_holes"]["count"] == 2


def test_the_ls1_assembly_places_everything_without_interference(tmp_path):
    """The only overlaps are the M1.2 screws forming their threads: four in
    the base's Pico posts, four in its wiring board pillars, two in the lid's
    stick pillars."""
    summary = _summary(build_part(LS1 / "assembly.py", tmp_path / "out"))
    pairs = sorted((i["a"].split("/")[-1], i["b"].split("/")[-1]) for i in summary["interference"])
    assert pairs == sorted([("base", f"pico_screw_{n}") for n in range(1, 5)]
                           + [("base", f"board_screw_{n}") for n in range(1, 5)]
                           + [(f"stick_screw_{n}", "lid") for n in range(1, 3)])
    assert all(i.get("thread") for i in summary["interference"])
    names = {c["name"].split("/")[-1] for c in summary["components"]}
    assert names == {"base", "single_18650_holder", "mt3608_boost", "bms_1s_3a",
                     "usb_c_breakout", "tsd_1166_button", "ws2812_stick_8", "pico_2w",
                     "buzzer", "ds18b20", "tp4056_charger", "wiring_board", "lid"} | {f"pico_screw_{n}" for n in range(1, 5)} \
        | {f"stick_screw_{n}" for n in range(1, 3)} | {f"board_screw_{n}" for n in range(1, 5)}
    touching = {(c["a"].split("/")[-1], c["b"].split("/")[-1]) for c in summary["contacts"]}
    assert ("ws2812_stick_8", "lid") in touching  # the stick against the skirt
    assert ("base", "tsd_1166_button") in touching  # the button body against the back wall
    assert ("base", "pico_2w") in touching  # the Pico on its posts
    assert ("base", "mt3608_boost") in touching  # the MT3608 in its slots
    assert ("single_18650_holder", "tp4056_charger") in touching  # the charger on the holder's rims


def test_the_ls1_schematic_names_only_real_pins_and_its_modelled_parts():
    """schematic.json passes the tool's checks, and every part it links names
    an item the assembled model places."""
    from cad.schematic import load
    data = load(LS1 / "schematic.json")
    script = "".join(p.read_text() for p in LS1.rglob("*.py"))
    for comp in data["components"]:
        if comp.get("item"):
            assert f'"{comp["item"]}"' in script, comp["ref"]


def test_the_wiring_board_holds_its_seven_parts_clear_of_each_other(tmp_path):
    """Three diodes, three resistors and the transistor, every lead through
    its hole: nothing overlaps."""
    summary = _summary(build_part(LS1 / "wiring_board" / "assembly.py", tmp_path / "wb"))
    assert summary["interference"] == []
    names = sorted(c["name"].split("/")[-1] for c in summary["components"])
    assert names == ["D1", "D2", "D3", "Q1", "R1", "R2", "R3", "board"]
    board = _summary(build_part(LS1 / "wiring_board" / "board" / "part.py", tmp_path / "b"))
    assert board["bounding_box"]["size"] == pytest.approx([35.56, 25.4, 1.6])
    assert board["regions"]["mount_holes"]["count"] == 4
    assert board["regions"]["diode_holes"]["count"] == 6
