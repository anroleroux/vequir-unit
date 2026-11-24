"""LS1 wiring board, assembled.

The perfboard with its parts in place, from its layout: the buzzer (BZ1)
sitting on the board on its pins; the DS18B20 (U5) and Q1 (BC337) standing
on their legs, their flats toward -y (the board's front edge); R1, R3, R4
and R5 (1/4 W, formed for 0.4 in) lying on it, R3 turned along the rows;
C1 (100 nF MLCC) standing on its leads; and J2, the 2 x 5 right-angle box
header, lying on it at its +x edge with its opening past that edge. The
parts come from vequir-standard's library.

Assumptions where the description is silent:
- every part stands on the board's top face; the leads go through and are
  cut 1.4 mm below its underside; solder is not modelled;
- the board stands on z = 0, as its own part does.
"""
import cadquery as cq

board = load_part("board")
resistor = load_library("electronics/resistor_025w")
npn = load_library("electronics/npn_bc337")
capacitor = load_library("electronics/capacitor_mlcc")
buzzer = load_library("electronics/buzzer_12x9")  # pins' tips on z = 0
sensor = load_library("electronics/ds18b20")  # formed: the board's top on z = 0
header = load_library("electronics/box_header_2x5")  # the board's top on z = 0, opening -y

top = board.thickness
shapes = {"R": (resistor.result, cq.Color(0.80, 0.70, 0.50)),
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
    if ref in board.along_rows:  # a quarter turn about z: its leads along y
        loc = cq.Location(cq.Vector(x, y, z), cq.Vector(0, 0, 1), 90)
    else:
        loc = cq.Location((x, y, z))
    result.add(shape, name=ref, loc=loc, color=color)

# J2: a quarter turn about z takes its rows (x) along the board's y, its row
# B (+y) to -x and its opening (-y) to +x, past the board's edge
result.add(header.result, name="J2",
           loc=cq.Location(cq.Vector(*board.header_centre, top), cq.Vector(0, 0, 1), 90),
           color=cq.Color(0.10, 0.10, 0.10))

regions = {}

if "show_object" in globals():  # CQ-editor (load_part runs under the CAD tool only)
    show_object(result, name="wiring_board")
