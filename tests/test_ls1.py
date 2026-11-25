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
    assert base["regions"]["usbc_pocket"]["count"] == 1  # the USB-C board's inset
    assert base["regions"]["board_slots"]["count"] == 2  # the wiring board's and the TP4056's
    assert base["regions"]["diode_bores"]["count"] == 3  # D1 above D2 above D3 in the pillar
    assert base["regions"]["long_tap_holes"]["count"] == 3  # the USB clamp's two, the board clamp's pillar
    assert base["regions"]["vents"]["count"] >= 20  # round holes
    assert base["regions"]["lid_screw_holes"]["count"] == 4  # two in each end wall


def test_the_ls1_lid_has_a_window_for_each_led(tmp_path):
    lid = _summary(build_part(LS1 / "lid" / "part.py", tmp_path / "lid"))
    assert lid["regions"]["led_windows"]["count"] == 8 * 4  # four sides each
    assert lid["regions"]["block_bottoms"]["count"] == 4  # a block at each end of each end wall
    assert lid["regions"]["block_tap_holes"]["count"] == 4
    assert lid["regions"]["stick_rests"]["count"] == 2  # in the stick's pocket
    assert lid["regions"]["header_shroud_top"]["count"] >= 1  # over J2
    assert lid["regions"]["lens_holes"]["count"] == 3  # two IR LEDs and the phototransistor
    assert lid["regions"]["ir_seats"]["count"] == 2  # a round seat for each IR LED's flange
    assert lid["regions"]["header_hole"]["count"] == 4  # J2's hole: four sides


def test_the_board_clamp_holds_both_boards(tmp_path):
    clamp = _summary(build_part(LS1 / "board_clamp" / "part.py", tmp_path / "bc"))
    assert clamp["regions"]["slot_bottoms"]["count"] == 2  # one on each board's top edge
    assert clamp["regions"]["screw_hole"]["count"] == 1


def test_the_ls1_assembly_places_everything_without_interference(tmp_path):
    """The only overlaps are the M1.2 screws forming their threads: four in
    the base's Pico posts, two in its USB clamp posts, one in the board
    clamp's pillar and four in the lid's corner blocks."""
    summary = _summary(build_part(LS1 / "assembly.py", tmp_path / "out"))
    pairs = sorted((i["a"].split("/")[-1], i["b"].split("/")[-1]) for i in summary["interference"])
    assert pairs == sorted([("base", f"pico_screw_{n}") for n in range(1, 5)]
                           + [("base", "board_clamp_screw")]
                           + [("base", f"clamp_screw_{n}") for n in range(1, 3)]
                           + [(f"lid_screw_{n}", "lid") for n in range(1, 5)])
    assert all(i.get("thread") for i in summary["interference"])
    names = {c["name"].split("/")[-1] for c in summary["components"]}
    assert names == {"base", "holder_18650_1s", "cell_18650", "mt3608_boost", "bms_1s_3a",
                     "usb_c_breakout", "tsd_1166_button", "ws2812_stick_8", "pico_2w",
                     "tp4056_charger", "wiring_board", "usb_clamp", "board_clamp", "board_clamp_screw",
                     "lid", "ir_led_1", "ir_led_2", "phototransistor"} | {f"pico_screw_{n}" for n in range(1, 5)} \
        | {f"r{n}_inline" for n in (7, 8, 9, 10)} \
        | {f"clamp_screw_{n}" for n in range(1, 3)} | {f"lid_screw_{n}" for n in range(1, 5)} \
        | {"d1_1n5822", "d2_1n5822", "d3_1n5822", "r2_inline", "r6_inline"}
    touching = {(c["a"].split("/")[-1], c["b"].split("/")[-1]) for c in summary["contacts"]}
    assert ("ws2812_stick_8", "lid") in touching  # the stick on its rests in the skirt's pocket
    assert ("holder_18650_1s", "cell_18650") in touching  # the cell in its holder
    for lens in ("ir_led_1", "ir_led_2", "phototransistor"):
        assert (lens, "lid") in touching  # its flange on the skirt's inside (the IR LEDs' on their seats)
    assert ("base", "tsd_1166_button") in touching  # the button body against the back wall
    assert ("base", "pico_2w") in touching  # the Pico on its posts
    assert ("base", "mt3608_boost") in touching  # the MT3608 in its slots
    assert ("base", "tp4056_charger") in touching  # the charger in its slot
    assert ("base", "wiring_board") in touching  # the wiring board in its slot
    assert ("tp4056_charger", "board_clamp") in touching  # the clamp on both top edges
    assert ("wiring_board", "board_clamp") in touching
    assert ("base", "board_clamp") in touching  # on its pillar
    assert ("usb_c_breakout", "usb_clamp") in touching  # the clamp pressing on the receptacle
    assert ("base", "usb_clamp") in touching  # and screwed to its posts
    comps = {c["name"].split("/")[-1]: c for c in summary["components"]}
    # the IR LEDs: above the stick's end LEDs, level with the phototransistor
    ph = comps["phototransistor"]
    for name in ("ir_led_1", "ir_led_2"):
        assert comps[name]["bounding_box_min"][2] == pytest.approx(ph["bounding_box_min"][2])
    front = comps["base"]["bounding_box_max"][0]
    assert comps["usb_c_breakout"]["bounding_box_max"][0] == pytest.approx(front - 0.4)  # in the wall
    inside = comps["base"]["bounding_box_max"][2] - 3.0  # the space above the floor
    # the wiring board stands 1 mm off the floor, right behind the USB-C board,
    # and the TP4056 lies behind it
    wb = comps["wiring_board"]
    assert wb["bounding_box_min"][2] == pytest.approx(3.0 + 1.0)
    assert wb["bounding_box_max"][2] < 3.0 + inside
    assert comps["tp4056_charger"]["bounding_box_max"][0] < wb["bounding_box_min"][0]
    # J2's face touches the lid's -y skirt from inside
    assert wb["bounding_box_min"][1] == pytest.approx(-comps["base"]["bounding_box_max"][1])
    # the TP4056 stands; D1 above D2 above D3, behind it
    tp, d2, d3 = comps["tp4056_charger"], comps["d2_1n5822"], comps["d3_1n5822"]
    assert tp["bounding_box_max"][2] - tp["bounding_box_min"][2] > 15
    assert d2["bounding_box_min"][0] == pytest.approx(d3["bounding_box_min"][0])
    assert d2["bounding_box_min"][2] > d3["bounding_box_min"][2] + 5
    assert d3["bounding_box_max"][0] < tp["bounding_box_min"][0]
    d1 = comps["d1_1n5822"]
    assert d1["bounding_box_min"][0] == pytest.approx(d3["bounding_box_min"][0])
    assert d1["bounding_box_min"][2] > d2["bounding_box_min"][2] + 5
    # 4 mm gaps: the diodes' -y ends to the lid, the Pico's USB end to the
    # button, the MT3608's +x end to the TP4056's parts
    half_b = comps["base"]["bounding_box_max"][1]
    assert d3["bounding_box_min"][1] == pytest.approx(-half_b + 4.0)
    assert comps["pico_2w"]["bounding_box_min"][0] == pytest.approx(comps["tsd_1166_button"]["bounding_box_max"][0] + 4.0)
    assert comps["mt3608_boost"]["bounding_box_max"][0] == pytest.approx(tp["bounding_box_min"][0] - 4.0)


def test_the_ls1_schematic_names_only_real_pins_and_its_modelled_parts():
    """schematic.json passes the tool's checks, and every part it links names
    an item the assembled model places."""
    from cad.schematic import load
    data = load(LS1 / "schematic.json")
    script = "".join(p.read_text() for p in LS1.rglob("*.py"))
    for comp in data["components"]:
        if comp.get("item"):
            assert f'"{comp["item"]}"' in script, comp["ref"]


def test_the_wiring_board_holds_its_parts_clear_of_each_other(tmp_path):
    """The buzzer, the DS18B20, four resistors, the capacitor, the
    transistor and the box header, every lead through its hole: nothing
    overlaps."""
    summary = _summary(build_part(LS1 / "wiring_board" / "assembly.py", tmp_path / "wb"))
    assert summary["interference"] == []
    names = sorted(c["name"].split("/")[-1] for c in summary["components"])
    assert names == ["BZ1", "C1", "J2", "Q1", "R1", "R3", "R4", "R5", "U5", "board"]
    board = _summary(build_part(LS1 / "wiring_board" / "board" / "part.py", tmp_path / "b"))
    assert board["bounding_box"]["size"] == pytest.approx([30.48, 22.86, 1.6])
    assert board["regions"]["buzzer_holes"]["count"] == 2
