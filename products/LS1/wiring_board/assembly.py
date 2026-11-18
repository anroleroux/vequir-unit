"""LS1 wiring board, assembled.

The perfboard with its parts in place, from its layout: D1, D2 and D3
(1N5822, formed for 0.6 in) lying along x, cathodes at +x; R1 to R6 (1/4 W,
formed for 0.4 in); Q1 (BC337) standing on its legs, its flat toward -y;
C1 (100 nF MLCC) standing on its leads; at the front, the buzzer (BZ1)
sitting on the board on its pins and the DS18B20 (U5) standing on its legs,
its flat toward -y (the board's front edge). The parts come from vequir-standard's library.

Assumptions where the description is silent:
- every part stands on the board's top face; the leads go through and are
  cut 1.4 mm below its underside; solder is not modelled;
- the board stands on z = 0, as its own part does.
"""
import cadquery as cq

board = load_part("board")
diode = load_library("electronics/diode_1n5822")
resistor = load_library("electronics/resistor_025w")
npn = load_library("electronics/npn_bc337")
capacitor = load_library("electronics/capacitor_mlcc")
buzzer = load_library("electronics/buzzer_12x9")  # pins' tips on z = 0
sensor = load_library("electronics/ds18b20")  # formed: the board's top on z = 0

top = board.thickness
shapes = {"D": (diode.result, cq.Color(0.10, 0.10, 0.10)),
          "R": (resistor.result, cq.Color(0.80, 0.70, 0.50)),
          "Q": (npn.result, cq.Color(0.10, 0.10, 0.10)),
          "C": (capacitor.result, cq.Color(0.25, 0.45, 0.75)),
          "B": (buzzer.result, cq.Color(0.10, 0.10, 0.10)),
          "U": (sensor.result, cq.Color(0.10, 0.10, 0.10))}

result = cq.Assembly(name="wiring_board").add(board.result, name="board",
                                              color=cq.Color(0.75, 0.62, 0.35))
for ref, (x, y) in board.centres.items():
    shape, color = shapes[ref[0]]
    z = top
    if ref.startswith("Q"):
        y -= npn.lead_y  # its legs on the row
    if ref.startswith("U"):
        y -= sensor.lead_y
    if ref.startswith("B"):
        z = top - buzzer.body_bottom  # its body on the board, its pins through it
    result.add(shape, name=ref, loc=cq.Location((x, y, z)), color=color)

regions = {}

if "show_object" in globals():  # CQ-editor (load_part runs under the CAD tool only)
    show_object(result, name="wiring_board")
