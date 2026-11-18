"""LS1 wiring board.

A perfboard cut to 14 x 20 holes on the 0.1 in (2.54 mm) grid, holding the
LS1's small through-hole parts: the buzzer (BZ1) and the DS18B20 (U5) in
the first rows, then D1, D2 and D3 (1N5822) lying along x in a column at the
-x end, R1, R2 and R3 (1/4 W) beside them, Q1 (BC337) below the resistors,
the battery divider (R4, R5 and C1) and the LED stick's data resistor (R6). Its layout (each part's centre and its holes) is here,
for the wiring board's assembly to place the parts on.

Assumptions where the description is silent:
- FR-4, 1.6 mm thick, plain 1.0 mm holes, the board's edges half a pitch
  outside the outer holes (35.56 x 50.8 mm);
- the diodes span six pitches (0.6 in) and the resistors four (0.4 in);
  rows: the buzzer's pins on row 4, columns 2 and 5 (its body centred
  between them, so its 7 mm pins reach the 7.62 mm holes, drilled to 1.3 mm),
  the DS18B20's legs on row 3, columns 9 to 11; the diodes on rows 8, 11
  and 14, R1 to R3 on rows 8, 10 and 12, the transistor's legs on row 14,
  columns 9 to 11; R4 and R5 on rows 16 and 18 beside them, R6 on row 17
  under the diodes, C1 (0.2 in) on row 19, columns 4 and 6; the corners
  are kept clear;
- the diodes' holes are drilled to 1.5 mm for their 1.3 mm leads, and the
  four corner holes to 1.3 mm (an M1.2 clearance);
- x along the 14 columns, y along the 10 rows; centred, standing on z = 0.
"""
import cadquery as cq

# in mm
pitch = 2.54  # 0.1 in grid
cols, rows = 14, 20
thickness = 1.6
hole = 1.0  # plain perfboard hole
diode_hole = 1.5  # drilled out for a 1N5822's 1.3 mm leads
buzzer_hole = 1.3  # drilled out so the buzzer's pins, 7 mm apart, reach holes 7.62 mm apart
mount_hole = 1.3  # drilled out at the corners, M1.2 clearance

length = cols * pitch  # along x
width = rows * pitch  # along y


def at(col, row):
    """A hole's centre, by column and row."""
    return ((col - (cols - 1) / 2) * pitch, (row - (rows - 1) / 2) * pitch)


# each part: (centre column, row) and the columns its leads go through
layout = {
    "BZ1": ((3.5, 4), (2, 5)), "U5": ((10, 3), (9, 10, 11)),
    "D1": ((3, 8), (0, 6)), "D2": ((3, 11), (0, 6)), "D3": ((3, 14), (0, 6)),
    "R1": ((10, 8), (8, 12)), "R2": ((10, 10), (8, 12)), "R3": ((10, 12), (8, 12)),
    "Q1": ((10, 14), (9, 10, 11)),
    "R4": ((10, 16), (8, 12)), "R5": ((10, 18), (8, 12)), "R6": ((3, 17), (1, 5)),
    "C1": ((5, 19), (4, 6)),
}
centres = {ref: at(*rc) for ref, (rc, _) in layout.items()}
diode_holes = [at(c, rc[1]) for ref, (rc, cs) in layout.items() if ref.startswith("D") for c in cs]
buzzer_holes = [at(c, layout["BZ1"][0][1]) for c in layout["BZ1"][1]]
mount_holes = [at(c, r) for c in (0, cols - 1) for r in (0, rows - 1)]
plain = [at(c, r) for c in range(cols) for r in range(rows)
         if at(c, r) not in diode_holes + mount_holes + buzzer_holes]

result = (
    cq.Workplane("XY").box(length, width, thickness, centered=(True, True, False))
    .faces(">Z").workplane().pushPoints(plain).hole(hole)
    .faces(">Z").workplane().pushPoints(diode_holes).hole(diode_hole)
    .faces(">Z").workplane().pushPoints(mount_holes).hole(mount_hole)
    .faces(">Z").workplane().pushPoints(buzzer_holes).hole(buzzer_hole)
)

regions = {
    "top": result.faces(">Z"),
    "mount_holes": result.faces("%CYLINDER").filter(  # the four corners
        lambda f: abs(f.BoundingBox().xlen - mount_hole) < 1e-3
        and min(abs(f.Center().x - x) + abs(f.Center().y - y) for x, y in mount_holes) < 1e-3),
    "buzzer_holes": result.faces("%CYLINDER").filter(
        lambda f: abs(f.BoundingBox().xlen - buzzer_hole) < 1e-3
        and min(abs(f.Center().x - x) + abs(f.Center().y - y) for x, y in buzzer_holes) < 1e-3),
    "diode_holes": result.faces("%CYLINDER").filter(
        lambda f: abs(f.BoundingBox().xlen - diode_hole) < 1e-3),
}

if "show_object" in globals():  # CQ-editor
    show_object(result, name="part")
