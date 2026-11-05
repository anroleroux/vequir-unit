"""PB6, the powerbank: its base, lid and assembled model.

The six-cell pack comes from vequir-power, and the charger boards and the
screws from vequir-standard; ``libraries.txt`` expects both beside this repository (CI
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
PB6 = PRODUCTS / "PB6"
MODEL = PB6 / "assembly.py"
BASE = PB6 / "base" / "part.py"


def _summary(result):
    assert result.ok, result.error
    return json.loads(result.files["summary"].read_text())


@pytest.fixture(autouse=True)
def _at_the_repository_root(monkeypatch):
    """``cad build`` takes designations relative to ``products/``."""
    monkeypatch.chdir(PRODUCTS.parent)


def test_discover_walks_the_real_catalogue():
    designations = [e.designation for e in discover(PRODUCTS)]
    assert designations == ["PB6", "PB6/base", "PB6/lid"]


def test_find_by_designation():
    assert find(PRODUCTS, "PB6/base/").script.name == "part.py"
    assert find(PRODUCTS, "PB6").script.name == "assembly.py"  # the product's own model
    assert find(PRODUCTS, "PB6/lid").part == "lid"
    with pytest.raises(KeyError):
        find(PRODUCTS, "PB6/nope")


def test_build_command_builds_one_part_by_designation(tmp_path, capsys):
    assert cli_main(["build", "PB6/base", "--out", str(tmp_path)]) == 0
    cad = tmp_path / "PB6" / "base" / "cad"
    assert (cad / "part.step").exists()
    assert "built PB6/base" in capsys.readouterr().out


def _only_thread_forming(summary):
    """The model's only interference: each pillar screw's 1.2 mm shank in its
    0.95 mm tap hole in the base, forming its thread (as in the pack)."""
    pairs = [(i["a"], i["b"]) for i in summary["interference"]]
    assert pairs == [("PB6/base", f"PB6/pillar_screw_{n}") for n in range(1, 9)]
    assert all(0 < i["volume_mm3"] < 2.0 and i.get("thread") for i in summary["interference"])


def test_the_pb6_base_carries_the_six_cell_pack_against_the_back_wall(tmp_path):
    """The six-cell pack from the library on the floor, its
    back end against the back (-x) wall, centred across the breadth, clear of
    the USB boards; no loose cells and no battery ribs any more."""
    summary = _summary(build_part(MODEL, tmp_path / "out"))
    base = _summary(build_part(BASE, tmp_path / "base"))
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
    summary = _summary(build_part(MODEL, tmp_path / "out"))
    base = _summary(build_part(BASE, tmp_path / "base"))
    (pack,) = [c for c in summary["components"] if c["name"].endswith("pack_3x2")]
    assert base["bounding_box"]["size"][1] == pytest.approx(
        pack["bounding_box_max"][1] - pack["bounding_box_min"][1])
    assert base["regions"]["pillar_tops"]["count"] == 4
    assert base["regions"]["tap_holes"]["count"] == 8
    screws = [c for c in summary["components"] if "pillar_screw_" in c["name"]]
    assert len(screws) == 8
    # the pack rests on the floor and on the four pillar tops
    (touch,) = [c for c in summary["contacts"] if c["b"].endswith("pack_3x2") and c["a"].endswith("/base")]
    assert touch["area_mm2"] > 0


def test_the_pb6_chargers_sit_behind_their_plug_holes(tmp_path):
    """The two IP6505 boards and the CN3302 board stand on the floor with their
    USB mouths against the inside of the front wall, each behind its own plug hole."""
    summary = _summary(build_part(MODEL, tmp_path / "out"))
    base = _summary(build_part(BASE, tmp_path / "base"))
    l, wall = base["bounding_box"]["size"][0], 3.0
    for name in ("ip6505_charger_1", "ip6505_charger_2", "cn3302_charger"):
        (board,) = [c for c in summary["components"] if c["name"].endswith(name)]
        assert board["bounding_box_max"][0] == pytest.approx(l / 2 - wall)
        assert board["bounding_box_min"][2] == pytest.approx(wall)
    assert base["regions"]["plug_holes"]["count"] == 8
    assert base["regions"]["usbc_hole"]["count"] == 4
    _only_thread_forming(summary)


def test_the_product_model_holds_the_enclosure_and_the_bought_in_parts(tmp_path):
    """PB6's one model holds its two parts (base and lid), the pack from
    vequir-power as one component, the three charger boards and the eight
    pillar screws from vequir-standard."""
    summary = _summary(build_part(MODEL, tmp_path / "out"))
    assert [c["name"] for c in summary["components"]] == [
        "PB6/base", "PB6/pack_3x2", "PB6/ip6505_charger_1", "PB6/ip6505_charger_2",
        "PB6/cn3302_charger", *[f"PB6/pillar_screw_{n}" for n in range(1, 9)], "PB6/lid"]
    (pack,) = [c for c in summary["components"] if c["name"] == "PB6/pack_3x2"]
    assert len(pack["meshes"]) > 1


def test_the_pb6_lid_fits_the_base(tmp_path):
    """The product model: the lid sits on the end walls' rims (+-x), its skirts
    close the open long sides (+-y), and its lips stay clear of the end walls
    and of the battery pack. The pack is as wide as the base, so the skirts
    also rest on the pack's sides."""
    summary = _summary(build_part(MODEL, tmp_path / "out"))
    box = _summary(build_part(BASE, tmp_path / "box"))
    assert not [i for i in summary["interference"] if "lid" in i["a"] + i["b"]]
    (lid,) = [c for c in summary["contacts"] if c["a"] == "PB6/base" and c["b"] == "PB6/lid"]
    l, b, h = box["bounding_box"]["size"]
    wall = 3.0
    rims = 2 * b * wall  # the two end walls' tops
    sides = 2 * (l * wall + 2 * wall * (h - wall))  # the floor's and end walls' edges at +-y
    assert lid["area_mm2"] >= rims + sides
    # the lid overhangs a = 5 mm at each end, adds its thickness each side and on top,
    # and reaches the base's bottom
    assert summary["bounding_box"]["size"] == pytest.approx([l + 10, b + 2 * wall, h + wall])
    assert summary["bounding_box"]["min"][2] == pytest.approx(0)


def test_build_command_takes_an_assembly_designation(tmp_path, capsys):
    assert cli_main(["build", "PB6", "--out", str(tmp_path)]) == 0
    assert (tmp_path / "PB6/_assembly/cad/part.step").exists()
    assert "built PB6" in capsys.readouterr().out
