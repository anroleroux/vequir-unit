"""PB6, the powerbank: its chassis, lid and assembled model.

The six-cell pack comes from vequir-power and the screws from
vequir-standard; ``libraries.txt`` expects both beside this repository (CI
clones them there).  Run from the repository root.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cad.catalog import discover, find
from cad.cli import main as cli_main
from cad.part import build_part

PRODUCTS = Path(__file__).resolve().parents[1] / "products"
CHASSIS = PRODUCTS / "PB6" / "chassis"


def _summary(result):
    assert result.ok, result.error
    return json.loads(result.files["summary"].read_text())


@pytest.fixture(autouse=True)
def _at_the_repository_root(monkeypatch):
    """``cad build`` takes designations relative to ``products/``."""
    monkeypatch.chdir(PRODUCTS.parent)


def test_discover_walks_the_real_catalogue():
    designations = [e.designation for e in discover(PRODUCTS)]
    assert designations == ["PB6/chassis", "PB6/chassis/base", "PB6/chassis/cn3302_charger", "PB6/chassis/ip6505_charger",
                            "PB6", "PB6/lid", "PICO2W/board"]


def test_find_by_designation():
    assert find(PRODUCTS, "PB6/chassis/base/").script.name == "part.py"
    assert find(PRODUCTS, "PB6/chassis").script.name == "assembly.py"
    assert find(PRODUCTS, "PB6").script.name == "assembly.py"  # the product's own model
    assert find(PRODUCTS, "PB6/lid").part == "lid"
    with pytest.raises(KeyError):
        find(PRODUCTS, "PB6/chassis/nope")


def test_build_command_builds_one_part_by_designation(tmp_path, capsys):
    assert cli_main(["build", "PB6/chassis/base", "--out", str(tmp_path)]) == 0
    cad = tmp_path / "PB6" / "chassis" / "base" / "cad"
    assert (cad / "part.step").exists()
    assert "built PB6/chassis/base" in capsys.readouterr().out


def _only_thread_forming(summary):
    """The chassis's only interference: each pillar screw's 1.2 mm shank in its
    0.95 mm tap hole in the base, forming its thread (as in the pack)."""
    pairs = [(i["a"], i["b"]) for i in summary["interference"]]
    assert pairs == [("chassis/base", f"chassis/pillar_screw_{n}") for n in range(1, 9)]
    assert all(0 < i["volume_mm3"] < 2.0 for i in summary["interference"])


def test_the_pb6_chassis_carries_the_six_cell_pack_against_the_back_wall(tmp_path):
    """The real chassis: the six-cell pack from the library on the floor, its
    back end against the back (-x) wall, centred across the breadth, clear of
    the USB boards; no loose cells and no battery ribs any more."""
    summary = _summary(build_part(CHASSIS / "assembly.py", tmp_path / "out"))
    base = _summary(build_part(CHASSIS / "base" / "part.py", tmp_path / "base"))
    _only_thread_forming(summary)
    names = [c["name"] for c in summary["components"]]
    assert not [n for n in names if "battery" in n]
    (pack,) = [c for c in summary["components"] if c["name"].endswith("pack_3x2")]
    l, wall = base["bounding_box"]["size"][0], 3.0
    assert pack["bounding_box_min"][0] == pytest.approx(-l / 2 + wall)  # against the back wall
    assert pack["bounding_box_min"][2] == pytest.approx(wall)  # on the floor
    assert pack["bounding_box_min"][1] == pytest.approx(-pack["bounding_box_max"][1])  # centred
    assert len([m for m in pack["meshes"] if m["name"].endswith("/battery")]) == 6
    assert "mini_wall_top" not in base["regions"]  # the front mini wall is gone
    assert not [n for n in names if "bms" in n]  # and so is the BMS


def test_the_pb6_pack_is_screwed_to_four_pillars(tmp_path):
    """The base is as wide as the pack; four pillars, one under each end strip
    tab, carry the tabs, each with two tap holes and two screws."""
    summary = _summary(build_part(CHASSIS / "assembly.py", tmp_path / "out"))
    base = _summary(build_part(CHASSIS / "base" / "part.py", tmp_path / "base"))
    (pack,) = [c for c in summary["components"] if c["name"].endswith("pack_3x2")]
    assert base["bounding_box"]["size"][1] == pytest.approx(
        pack["bounding_box_max"][1] - pack["bounding_box_min"][1])
    assert base["regions"]["pillar_tops"]["count"] == 4
    assert base["regions"]["tap_holes"]["count"] == 8
    screws = [c for c in summary["components"] if "pillar_screw_" in c["name"]]
    assert len(screws) == 8
    # the pack rests on the floor and on the four pillar tops
    (touch,) = [c for c in summary["contacts"] if c["b"].endswith("pack_3x2")]
    assert touch["a"] == "chassis/base" and touch["area_mm2"] > 0


def test_the_pb6_chargers_sit_behind_their_plug_holes(tmp_path):
    """The two IP6505 boards and the CN3302 board stand on the floor with their
    USB mouths against the inside of the front wall, each behind its own plug hole."""
    summary = _summary(build_part(CHASSIS / "assembly.py", tmp_path / "out"))
    base = _summary(build_part(CHASSIS / "base" / "part.py", tmp_path / "base"))
    l, wall = base["bounding_box"]["size"][0], 3.0
    for name in ("ip6505_charger_1", "ip6505_charger_2", "cn3302_charger"):
        (board,) = [c for c in summary["components"] if c["name"].endswith(name)]
        assert board["bounding_box_max"][0] == pytest.approx(l / 2 - wall)
        assert board["bounding_box_min"][2] == pytest.approx(wall)
    assert base["regions"]["plug_holes"]["count"] == 8
    assert base["regions"]["usbc_hole"]["count"] == 4
    _only_thread_forming(summary)


def test_the_product_model_lists_only_what_it_holds_directly(tmp_path):
    """PB6's model holds the chassis (a sub-assembly) and the lid: those are its
    two components, the chassis one for all its parts; every part is still
    drawn, in its own mesh and colour, inside the chassis."""
    summary = _summary(build_part(PRODUCTS / "PB6" / "assembly.py", tmp_path / "out"))
    assert [c["name"] for c in summary["components"]] == ["PB6/chassis", "PB6/lid"]
    chassis, lid = summary["components"]
    assert "PB6/chassis/cn3302_charger" in [m["name"] for m in chassis["meshes"]]
    assert len(chassis["meshes"]) > 1 and len(lid["meshes"]) == 1
    assert all(c["a"] == "PB6/chassis" and c["b"] == "PB6/lid" for c in summary["contacts"])


def test_the_pb6_lid_fits_the_base(tmp_path):
    """The product model: the lid sits on the end walls' rims (+-x), its skirts
    close the open long sides (+-y), and its lips stay clear of the end walls
    and of the battery pack. The pack is as wide as the base, so the skirts
    also rest on the pack's sides."""
    summary = _summary(build_part(PRODUCTS / "PB6" / "assembly.py", tmp_path / "out"))
    box = _summary(build_part(CHASSIS / "base" / "part.py", tmp_path / "box"))
    assert summary["interference"] == []
    (lid,) = [c for c in summary["contacts"] if c["b"].endswith("/lid")]
    l, b, h = box["bounding_box"]["size"]
    wall = 3.0
    rims = 2 * b * wall  # the two end walls' tops
    sides = 2 * (l * wall + 2 * wall * (h - wall))  # the floor's and end walls' edges at +-y
    assert lid["a"] == "PB6/chassis" and lid["area_mm2"] > rims + sides
    # the lid overhangs a = 5 mm at each end, adds its thickness each side and on top,
    # and reaches the base's bottom
    assert summary["bounding_box"]["size"] == pytest.approx([l + 10, b + 2 * wall, h + wall])
    assert summary["bounding_box"]["min"][2] == pytest.approx(0)


def test_build_command_takes_an_assembly_designation(tmp_path, capsys):
    assert cli_main(["build", "PB6/chassis", "--out", str(tmp_path)]) == 0
    assert (tmp_path / "PB6/chassis/_assembly/cad/part.step").exists()
    assert "built PB6/chassis" in capsys.readouterr().out


def test_the_pico_2_w_has_its_pins_and_mounting_holes(tmp_path):
    """51 x 21 mm on a 1 mm board, the micro-USB 1.3 mm proud of its end; 40
    pin holes, 40 castellations, 4 mounting holes and 3 debug pads."""
    summary = _summary(build_part(PRODUCTS / "PICO2W/board/part.py", tmp_path / "out"))
    assert summary["bounding_box"]["size"] == pytest.approx([52.3, 21.0, 3.6])
    assert summary["face_types"]["CYLINDER"] == 40 + 40 + 4 + 3
    assert summary["regions"]["mounting_holes"]["count"] == 4
    assert summary["regions"]["pin_strips"]["count"] == 2
    assert summary["regions"]["debug_pads"]["count"] == 1
