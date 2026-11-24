"""LS1 lid.

A cover that sits on the rim of the base box and wraps down its two long
sides, like the PB6 lid: a top plate with a skirt down each side, past the
box's breadth by the lid's thickness and down to the bottom of the base,
overhanging the box by a = 5 mm at both ends, and four blocks under the
plate, one at each end of the front (+x) and back (-x) end walls, just
inside them; an M1.2 x 6 countersunk screw through the end wall from the
outside goes into a tap hole in each. The +y skirt has eight square
windows in a row, one for each LED of the WS2812 stick
(electronics/ws2812_stick_8), which sits, LEDs out, in a shallow pocket in
the skirt's inside face on two little rests, unscrewed for now; R6, inline
at its data input, lies in the pocket too. The -y skirt has a rectangular hole for the
wiring board's 10-pin box header (J2), whose face touches the skirt's
inside, so a ribbon cable's socket plugs in from outside; a shroud on the
skirt's inside runs over the header's top and down its front (+x) and
rear (-x) sides, open at the bottom so the lid lifts off over it.
It is sized from the box and the stick, and the stick's place comes from
the box, which lays out everything inside.

Assumptions where the description is silent:
- the lid's thickness (plate and skirts) is the box's wall thickness; the
  skirts touch the box's open sides;
- each block is 4 mm along x, 5 mm across (from the skirt in) and 6 mm deep
  under the plate (the box's lid_block_t, lid_block_w and lid_block_depth),
  its outer face 0.2 mm inside its end wall; its M1.2 tap hole (0.95 mm),
  3.5 mm deep along x, is centred on the block's face, in line with the
  box's countersunk hole;
- the stick runs along x, in front of the Pico, its centre line 18 mm above
  the bottom (the box's stick_x, stick_y and stick_z), clear of the lips;
- the pocket is the stick's board (and R6 beyond its -x end) with 0.2 mm
  clearance all round, 1.0 mm deep into the 3 mm skirt (the box's
  stick_inset); in it, a rest 2.4 mm square and 0.6 mm tall (stick_rest)
  under each of the stick's mounting holes holds its LED side off the
  pocket's floor, so its 0.5 mm capacitors clear it and its board is
  0.4 mm into the pocket, its LEDs 1.0 mm into their windows; the stick is
  not screwed for now (glue it, or the holes are there for later);
- each window is the LED (5 mm square) with 0.2 mm clearance all round,
  square through the skirt;
- the header's hole is J2's shroud (20.3 mm up the height, 8.9 mm along
  x) with 0.2 mm clearance all round, square through the -y skirt, in line
  with the shroud (the box's header_* values);
- J2's shroud is 1.2 mm thick, 0.2 mm clear of J2: its top wall from the
  skirt to 0.2 mm past J2's back; its front wall the same depth, from J2's
  bottom up; its rear wall only where J2 stands past the wiring board's
  edge (the board itself is behind the rest of J2); the top wall is cut
  back 0.2 mm round the board and the board clamp, which it passes over;
- modelled as installed, centred like the box: the skirt bottoms stand on
  z = 0 and the plate's underside is at seat_height = the box's h.
"""
import cadquery as cq

box = load_part("../base")  # the box this lid fits: l, b, h, wall
stick = load_library("electronics/ws2812_stick_8")  # the LED stick behind the windows

# parameters, in mm
t = box.wall  # lid thickness: plate and skirts
a = 5.0  # overhang past the box at each end, along the length
block_t, block_w, block_depth = box.lid_block_t, box.lid_block_w, box.lid_block_depth
clearance = box.lid_clearance  # between each block and the inside of its end wall
block_tap = 3.5  # each block's tap hole, along x
window_clearance = 0.2  # all round each LED, in its window
header_clearance = 0.2  # all round J2's shroud, in its hole
tap_drill = 0.95  # M1.2 x 0.25, the blocks' tap holes
rest = 2.4  # the stick's rests in its pocket, square
pocket_clearance = 0.2  # round the stick and R6, in the pocket
shroud_wall = 1.2  # J2's shroud
shroud_clearance = 0.2  # round J2, and round what the shroud passes over
stick_x, stick_y, stick_z = box.stick_x, box.stick_y, box.stick_z  # the stick's place

length = box.l + 2 * a  # overall, along x
breadth = box.b + 2 * t  # overall, along y
seat_height = box.h  # the plate's underside, on the box rim
height = seat_height + t  # overall
block_outer = box.l / 2 - box.wall - clearance  # each block's outer face, from the centre

# the stick, LEDs facing +y and its -y edge turned to the top: the windows' centres
window = stick.led + 2 * window_clearance  # square
window_z = stick_z - stick.led_y  # the stick's -y edge is turned to the top
window_xs = [stick_x + x for x in stick.led_xs]
assert abs(stick_x) + stick.length / 2 < block_outer - block_t, "the stick runs into a block"
assert stick_z + stick.width / 2 < seat_height, "the stick reaches the plate"

cover = (
    cq.Workplane("XY")
    .box(length, breadth, height, centered=(True, True, False))
    .cut(cq.Workplane("XY").box(length, box.b, seat_height, centered=(True, True, False)))
)
block_x = block_outer - block_t / 2
block_y = box.b / 2 - block_w / 2
blocks = (
    cq.Workplane("XY", origin=(0, 0, seat_height - block_depth))
    .pushPoints([(sx * block_x, sy * block_y) for sx in (-1, 1) for sy in (-1, 1)])
    .rect(block_t, block_w)
    .extrude(block_depth)
)
block_taps = None
for x, y, z in box.lid_screws:  # each from the block's outer face, inward
    side = 1 if x > 0 else -1
    tap = (cq.Workplane("YZ", origin=(side * block_outer, y, z)).circle(tap_drill / 2)
           .extrude(-side * block_tap))
    block_taps = tap if block_taps is None else block_taps.union(tap)
windows = (
    cq.Workplane("XZ", origin=(0, box.b / 2, 0))  # normal -y: extrude toward -y
    .pushPoints([(x, window_z) for x in window_xs])
    .rect(window, window)
    .extrude(-t)  # outward, through the +y skirt
)
# the stick's pocket in the +y skirt (and R6's, at its -x end), and its rests
pocket_x0 = box.r6_x - box.inline.length / 2 - pocket_clearance
pocket_x1 = stick_x + stick.length / 2 + pocket_clearance
pocket_z0 = stick_z - stick.width / 2 - pocket_clearance
pocket_z1 = stick_z + stick.width / 2 + pocket_clearance
pocket = (cq.Workplane("XY", origin=(pocket_x0, box.b / 2, pocket_z0))
          .box(pocket_x1 - pocket_x0, box.stick_inset, pocket_z1 - pocket_z0, centered=False))
rests = (
    cq.Workplane("XZ", origin=(0, box.b / 2 + box.stick_inset, 0))  # normal -y: toward the stick
    .pushPoints(box.stick_holes)
    .rect(rest, rest)
    .extrude(box.stick_rest)
)
assert box.stick_inset < t, "the stick's pocket goes through the skirt"
# J2's hole, through the -y skirt
hx0 = box.wb_back_x + box.wb.thickness - header_clearance
hx1 = box.header_x1 + header_clearance
hz0 = box.header_z0 - header_clearance
hz1 = box.header_z1 + header_clearance
header_hole = (cq.Workplane("XY", origin=(hx0, -box.b / 2 - t, hz0))
               .box(hx1 - hx0, t, hz1 - hz0, centered=False))
assert hx1 < block_outer - block_t, "the header's hole runs into a block"

# J2's shroud on the -y skirt's inside: a top wall, a front (+x) wall and a
# rear (-x) wall past the wiring board's edge; open at the bottom
c, w = shroud_clearance, shroud_wall
jx0, jx1 = box.wb_back_x + box.wb.thickness, box.header_x1  # J2, along x
jz0, jz1 = box.header_z0, box.header_z1
sy0 = -box.b / 2  # the skirt's inside
sy1 = sy0 + box.header_depth + c  # past J2's back
board_edge = box.wb_y - box.wb.length / 2  # the wiring board's -y edge


def slab(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY", origin=(x0, y0, z0)).box(x1 - x0, y1 - y0, z1 - z0, centered=False)


shroud = (slab(jx0 - c - w, jx1 + c + w, sy0, sy1, jz1 + c, jz1 + c + w)  # over J2's top
          .union(slab(jx1 + c, jx1 + c + w, sy0, sy1, jz0, jz1 + c))  # its front side
          .union(slab(jx0 - c - w, jx0 - c, sy0, board_edge - c, jz0, jz1 + c)))  # its rear, past the board
keep_out = (slab(box.wb_back_x - c, jx0 + c, board_edge - c, sy1 + c, jz0, height)  # the board
            .union(slab(box.tp_slot_x[0] - box.rail_wall - c, box.wb_slot_x[1] + box.rail_wall + c,
                        box.pillar_y - box.bc_w / 2 - c, box.pillar_y + box.bc_w / 2 + c,
                        box.charger_top - box.rail_engage - c, box.bc_top + c)))  # the board clamp
shroud = shroud.cut(keep_out)
assert jz1 + c + w < seat_height, "J2's shroud reaches the plate"

result = (cover.union(blocks).cut(block_taps).cut(windows).cut(pocket).union(rests)
          .cut(header_hole).union(shroud))

regions = {
    "top": result.faces(">Z"),
    "skirts_inside": result.faces("%PLANE").filter(  # against the box's open sides
        lambda f: abs(f.normalAt().y) > 0.999 and abs(abs(f.Center().y) - box.b / 2) < 1e-6),
    "block_bottoms": result.faces("%PLANE").filter(
        lambda f: f.normalAt().z < -0.999 and abs(f.Center().z - (seat_height - block_depth)) < 1e-6),
    "block_tap_holes": result.faces("%CYLINDER").filter(
        lambda f: abs(f.BoundingBox().xlen - block_tap) < 1e-3),
    "led_windows": result.faces("%PLANE").filter(  # the windows' four sides each
        lambda f: abs(f.normalAt().y) < 1e-6 and box.b / 2 + 1e-6 < f.Center().y < box.b / 2 + t - 1e-6
        and abs(f.Center().z - window_z) < window),
    "stick_rests": result.faces("%PLANE").filter(  # where the stick's board rests
        lambda f: f.normalAt().y < -0.999
        and abs(f.Center().y - (box.b / 2 + box.stick_inset - box.stick_rest)) < 1e-6),
    "header_hole": result.faces("%PLANE").filter(  # its four sides
        lambda f: abs(f.Center().y + box.b / 2 + t / 2) < 1e-6 and abs(f.normalAt().y) < 1e-6
        and hx0 - 1e-6 <= f.Center().x <= hx1 + 1e-6 and hz0 - 1e-6 <= f.Center().z <= hz1 + 1e-6),
    "header_shroud_top": result.faces("%PLANE").filter(  # its underside, over J2
        lambda f: f.normalAt().z < -0.999 and abs(f.Center().z - (jz1 + c)) < 1e-6),
}

if "show_object" in globals():  # CQ-editor (load_part runs under the CAD tool only)
    show_object(result, name="part")
