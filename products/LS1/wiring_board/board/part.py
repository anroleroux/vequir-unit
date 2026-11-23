"""LS1 wiring board.

A perfboard cut to 12 x 9 holes on the 0.1 in (2.54 mm) grid, as small as
the LS1's remaining board parts allow: the buzzer (BZ1) at the front left
corner, the DS18B20 (U5) and Q1 (BC337) along the front edge beside it, R4,
R5 and R1 (the divider's top and bottom, and the one-wire pull-up) in a
column behind them, and R3 (Q1's base resistor) and C1 (the divider's
capacitor) behind the buzzer. D1 is soldered on the MT3608, D2 and D3 lie
on the floor, and R2 and R6 are soldered inline at the button and the LED
stick. Its layout (each part's centre and its holes) is here, for the
wiring board's assembly to place the parts on.

Assumptions where the description is silent:
- FR-4, 1.6 mm thick, plain 1.0 mm holes, the board's edges half a pitch
  outside the outer holes (30.48 x 22.86 mm);
- the buzzer's pins on row 2, columns 1 and 4 (its body centred between
  them, so its 7 mm pins reach the 7.62 mm holes, drilled to 1.3 mm), its
  body reaching to the board's front edge; the DS18B20's legs on row 1,
  columns 6 to 8, and Q1's on row 1, columns 9 to 11; R4, R5 and R1 span
  four pitches (0.4 in) on rows 3, 5 and 7, columns 6 to 10; R3 on row 6,
  columns 0 to 4; C1 (0.2 in) on row 8, columns 1 and 3; the four corners
  are kept clear;
- the four corner holes are drilled to 1.3 mm (an M1.2 clearance);
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
mount_hole = 1.3  # drilled out at the corners, M1.2 clearance

length = cols * pitch  # along x
width = rows * pitch  # along y


def at(col, row):
    """A hole's centre, by column and row."""
    return ((col - (cols - 1) / 2) * pitch, (row - (rows - 1) / 2) * pitch)


# each part: (centre column, row) and the columns its leads go through
layout = {
    "BZ1": ((2.5, 2), (1, 4)), "U5": ((7, 1), (6, 7, 8)), "Q1": ((10, 1), (9, 10, 11)),
    "R4": ((8, 3), (6, 10)), "R5": ((8, 5), (6, 10)), "R1": ((8, 7), (6, 10)),
    "R3": ((2, 6), (0, 4)), "C1": ((2, 8), (1, 3)),
}
centres = {ref: at(*rc) for ref, (rc, _) in layout.items()}
buzzer_holes = [at(c, layout["BZ1"][0][1]) for c in layout["BZ1"][1]]
mount_holes = [at(c, r) for c in (0, cols - 1) for r in (0, rows - 1)]
plain = [at(c, r) for c in range(cols) for r in range(rows)
         if at(c, r) not in mount_holes + buzzer_holes]

result = (
    cq.Workplane("XY").box(length, width, thickness, centered=(True, True, False))
    .faces(">Z").workplane().pushPoints(plain).hole(hole)
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
}

if "show_object" in globals():  # CQ-editor
    show_object(result, name="part")
