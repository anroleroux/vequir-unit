"""LS1 wiring board.

A perfboard cut to 12 x 9 holes on the 0.1 in (2.54 mm) grid. Its parts
are packed into the nine columns at one side (columns 0 to 8, toward the
box's +y side when it stands in the LS1): the buzzer (BZ1) at the front,
the DS18B20 (U5) beside it, Q1 (BC337) below that, R4, R5 and R1 (the
divider's top and bottom, and the one-wire pull-up) in rows under the
buzzer, R3 (Q1's base resistor) standing along the rows at the inner side,
and C1 (the divider's capacitor) beside R5. Column 9 stays empty, behind
the base's clamp pillar, and the last two columns (10 and 11) take the
2 x 5 right-angle box header (J2), its opening past the board's edge.
D1, D2 and D3 sit in the base's diode pillar, and R2 and R6 are wired in
at the button and the LED stick. Its layout (each part's centre and its
holes) is here, for the wiring board's assembly to place the parts on.

Assumptions where the description is silent:
- FR-4, 1.6 mm thick, plain 1.0 mm holes, the board's edges half a pitch
  outside the outer holes (30.48 x 22.86 mm); the board stands in a slot
  along its back edge (row 8) and is clamped at its front edge (row 0), so
  it has no screw holes, and rows 0 and 8 are kept clear of parts;
- the buzzer's pins on row 2, columns 1 and 4 (its body centred between
  them, so its 7 mm pins reach the 7.62 mm holes, drilled to 1.3 mm); the
  DS18B20's legs on row 1, columns 6 to 8, and Q1's on row 4, columns 5 to
  7; R4, R5 and R1 span four pitches (0.4 in) on rows 5, 6 and 7, columns
  0 to 4; R3 spans rows 3 to 7 in column 8; C1 (0.2 in) on row 6, columns
  5 and 7;
- J2's row A (nearer its opening) in column 11 and row B in column 10, its
  five pins on rows 2 to 6, its opening toward the board's +x edge;
- x along the 12 columns, y along the 9 rows (row 0 at -y, the front);
  centred, standing on z = 0.
"""
import cadquery as cq

# in mm
pitch = 2.54  # 0.1 in grid
cols, rows = 12, 9
thickness = 1.6
hole = 1.0  # plain perfboard hole
buzzer_hole = 1.3  # drilled out so the buzzer's pins, 7 mm apart, reach holes 7.62 mm apart

length = cols * pitch  # along x
width = rows * pitch  # along y


def at(col, row):
    """A hole's centre, by column and row."""
    return ((col - (cols - 1) / 2) * pitch, (row - (rows - 1) / 2) * pitch)


# each part: (centre column, row) and the columns its leads go through (or,
# for a part in `along_rows`, the rows, in its centre column)
layout = {
    "BZ1": ((2.5, 2), (1, 4)), "U5": ((7, 1), (6, 7, 8)), "Q1": ((6, 4), (5, 6, 7)),
    "R4": ((2, 5), (0, 4)), "R5": ((2, 6), (0, 4)), "R1": ((2, 7), (0, 4)),
    "R3": ((8, 5), (3, 7)), "C1": ((6, 6), (5, 7)),
}
along_rows = {"R3"}
centres = {ref: at(*rc) for ref, (rc, _) in layout.items()}
buzzer_holes = [at(c, layout["BZ1"][0][1]) for c in layout["BZ1"][1]]
# J2, the 2 x 5 box header: row A in column 11, row B in column 10, rows 2 to 6
header_cols = (11, 10)  # its rows A and B
header_rows = range(2, 7)
header_centre = at(header_cols[0], 4)  # its row A's middle pin
plain = [at(c, r) for c in range(cols) for r in range(rows) if at(c, r) not in buzzer_holes]

result = (
    cq.Workplane("XY").box(length, width, thickness, centered=(True, True, False))
    .faces(">Z").workplane().pushPoints(plain).hole(hole)
    .faces(">Z").workplane().pushPoints(buzzer_holes).hole(buzzer_hole)
)

regions = {
    "top": result.faces(">Z"),
    "buzzer_holes": result.faces("%CYLINDER").filter(
        lambda f: abs(f.BoundingBox().xlen - buzzer_hole) < 1e-3
        and min(abs(f.Center().x - x) + abs(f.Center().y - y) for x, y in buzzer_holes) < 1e-3),
}

if "show_object" in globals():  # CQ-editor
    show_object(result, name="part")
