"""LS1 lid.

A cover that sits on the rim of the base box and wraps down its two long
sides, like the PB6 lid: a top plate with a skirt down each side, past the
box's breadth by the lid's thickness and down to the bottom of the base,
overhanging the box by a = 5 mm at both ends, and four blocks under the
plate, one at each end of the front (+x) and back (-x) end walls, just
inside them; an M1.2 x 6 countersunk screw through the end wall from the
outside goes into a tap hole in each. The +y
skirt has eight square windows in a row, one for each LED of the WS2812
stick (electronics/ws2812_stick_8), which is screwed, LEDs out, to two
little pillars on the skirt's inside face with M1.2 x 3 countersunk screws.
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
- the two pillars are 2.4 mm square and 0.6 mm tall (the box's
  stick_standoff), one under each of the stick's mounting holes, so its
  0.5 mm capacitors clear the skirt and each LED reaches 1.0 mm into its
  window; each has an M1.2 tap hole (0.95 mm) 2.0 mm deep, through the
  pillar and 1.4 mm into the skirt, for an M1.2 x 3 screw through the
  stick's 2.0 mm hole from behind;
- each window is the LED (5 mm square) with 0.2 mm clearance all round,
  square through the skirt;
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
pillar = 2.4  # the stick's pillars, square
tap_drill = 0.95  # M1.2 x 0.25
tap_depth = 2.0  # from the pillar's face
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
pillars = (
    cq.Workplane("XZ", origin=(0, box.b / 2, 0))  # normal -y: toward the stick
    .pushPoints(box.stick_holes)
    .rect(pillar, pillar)
    .extrude(box.stick_standoff)
)
taps = (
    cq.Workplane("XZ", origin=(0, box.b / 2 - box.stick_standoff, 0))
    .pushPoints(box.stick_holes)
    .circle(tap_drill / 2)
    .extrude(-tap_depth)  # toward +y, into the pillar and the skirt
)
result = cover.union(blocks).cut(block_taps).cut(windows).union(pillars).cut(taps)

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
    "stick_pillars": result.faces("%PLANE").filter(  # where the stick's board rests
        lambda f: f.normalAt().y < -0.999
        and abs(f.Center().y - (box.b / 2 - box.stick_standoff)) < 1e-6),
    "tap_holes": result.faces("%CYLINDER").filter(  # the stick's
        lambda f: abs(f.BoundingBox().xlen - tap_drill) < 1e-3
        and abs(f.BoundingBox().ylen - tap_depth) < 1e-3),
}

if "show_object" in globals():  # CQ-editor (load_part runs under the CAD tool only)
    show_object(result, name="part")
