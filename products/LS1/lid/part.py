"""LS1 lid.

A cover that sits on the rim of the base box and wraps down its two long
sides, like the PB6 lid: a top plate with a skirt down each side, past the
box's breadth by the lid's thickness and down to the bottom of the base,
overhanging the box by a = 5 mm at both ends, and a lip under the plate at
the front (+x) and the back (-x), just inside the box's end walls. The +y
skirt has eight square windows in a row, one for each LED of the WS2812
stick (electronics/ws2812_stick_8) that sits against its inside face, LEDs
out. It is sized from the box and the stick.

Assumptions where the description is silent:
- the lid's thickness (plate and skirts) is the box's wall thickness; the
  skirts touch the box's open sides; each lip is one wall thick, 6 mm deep,
  across the full breadth, its outer face 0.2 mm inside its end wall (as on
  the PB6 lid);
- the stick runs along x, centred on the lid's length, its centre line
  18 mm above the bottom: above the MT3608 and clear of the lid's lips;
- the stick's capacitors (its tallest parts beside the LEDs) rest on the
  skirt's inside face, so each LED reaches 1.1 mm into its window; each
  window is the LED (5 mm square) with 0.2 mm clearance all round, square
  through the skirt; how the stick is held there is not modelled;
- modelled as installed, centred like the box: the skirt bottoms stand on
  z = 0 and the plate's underside is at seat_height = the box's h.
"""
import cadquery as cq

box = load_part("../base")  # the box this lid fits: l, b, h, wall
stick = load_library("electronics/ws2812_stick_8")  # the LED stick behind the windows

# parameters, in mm
t = box.wall  # lid thickness: plate and skirts
a = 5.0  # overhang past the box at each end, along the length
lip_depth = 6.0  # how far the lips drop below the plate
lip_wall = box.wall  # lip thickness, along x
clearance = 0.2  # between each lip and the inside of its end wall
window_clearance = 0.2  # all round each LED, in its window
stick_x = 0.0  # the stick's centre, along x
stick_z = 18.0  # the stick's centre line, above the bottom

length = box.l + 2 * a  # overall, along x
breadth = box.b + 2 * t  # overall, along y
seat_height = box.h  # the plate's underside, on the box rim
height = seat_height + t  # overall
lip_span = box.l - 2 * box.wall - 2 * clearance  # across the lips' outer faces
lip_length = box.b  # each lip's length, along y

# the stick, LEDs facing +y: its underside's plane, and the windows' centres
stick_y = box.b / 2 - stick.cap_top  # its underside, so the capacitors touch the skirt
window = stick.led + 2 * window_clearance  # square
window_z = stick_z - stick.led_y  # the stick's -y edge is turned to the top
window_xs = [stick_x + x for x in stick.led_xs]
assert stick_z + stick.width / 2 < seat_height - lip_depth or \
    abs(stick_x) + stick.length / 2 < lip_span / 2 - lip_wall, "the stick runs into a lip"
assert stick_z + stick.width / 2 < seat_height, "the stick reaches the plate"

cover = (
    cq.Workplane("XY")
    .box(length, breadth, height, centered=(True, True, False))
    .cut(cq.Workplane("XY").box(length, box.b, seat_height, centered=(True, True, False)))
)
lip_x = lip_span / 2 - lip_wall / 2
lips = (
    cq.Workplane("XY", origin=(0, 0, seat_height - lip_depth))
    .pushPoints([(lip_x, 0), (-lip_x, 0)])
    .rect(lip_wall, lip_length)
    .extrude(lip_depth)
)
windows = (
    cq.Workplane("XZ", origin=(0, box.b / 2, 0))  # normal -y: extrude toward -y
    .pushPoints([(x, window_z) for x in window_xs])
    .rect(window, window)
    .extrude(-t)  # outward, through the +y skirt
)
result = cover.union(lips).cut(windows)

regions = {
    "top": result.faces(">Z"),
    "skirts_inside": result.faces("%PLANE").filter(  # against the box's open sides
        lambda f: abs(f.normalAt().y) > 0.999 and abs(abs(f.Center().y) - box.b / 2) < 1e-6),
    "lip_bottoms": result.faces("%PLANE").filter(
        lambda f: f.normalAt().z < -0.999 and abs(f.Center().z - (seat_height - lip_depth)) < 1e-6),
    "led_windows": result.faces("%PLANE").filter(  # the windows' four sides each
        lambda f: box.b / 2 + 1e-6 < f.Center().y < box.b / 2 + t - 1e-6
        and abs(f.Center().z - window_z) < window),
}

if "show_object" in globals():  # CQ-editor (load_part runs under the CAD tool only)
    show_object(result, name="part")
