"""LS1 base box.

A floor and two end walls, open at the top and along both long sides, like
the PB6 base but for one cell: a single 18650 holder from the parts library
(battery_holders/single_18650_holder) on the floor against the back wall
along the -y side; beside it at +y an MT3608 boost board, and in front of
that the single-cell BMS strip; in front of the holder a horizontal USB-C
breakout board with its receptacle behind a USB-C plug hole in the front
wall; and a round hole in the back wall for the TSD-1166 LED push button.
The box is sized from the parts, so it follows a change to any of them.

Assumptions where the description is silent:
- l, b and h are outside dimensions, the floor is as thick as the walls,
  wall = 3 and h = 30 mm (as tall as needed for the holder, the button and
  the LED stick on the lid); l and b follow from the parts below;
- the holder stands on the floor, its back end (the clips' lugs) against
  the back wall and its -y side flush with the box's -y side; it is not
  fixed to the floor yet (no pillars or screws);
- the MT3608 lies 1 mm from the back wall and 2 mm in from the +y side,
  2 mm clear of the holder, VIN at the front; the BMS lies on the floor 2 mm
  in front of it, on the same centre line; their wiring is not modelled;
- the USB-C breakout lies on the floor centred across the breadth, at least
  1 mm in front of the holder; its plug hole is the USB-C plug's
  8.25 x 2.4 mm shell with 0.5 mm clearance all round, round-ended, as on the
  PB6;
- the button's hole is its 10 mm button plus 0.3 mm all round (10.6 mm),
  its axis 8 mm in from the +y side (2 mm clear of the button's body) and
  high enough for the body (12 mm square) to clear the MT3608 below it by
  1 mm; the body rests against the inside of the back wall, so its button
  stands 2 mm proud of the wall; how the body is held is not modelled;
- the box is centred on x and y and stands on z = 0, l along x (+x the
  front), b along y; corners are sharp.
"""
import cadquery as cq

holder = load_library("battery_holders/single_18650_holder")  # the cell in its holder
boost = load_library("power/mt3608_boost")  # 36 x 17 boost board
bms = load_library("power/bms_1s_3a")  # 30.3 x 3.7 protection strip
usbc = load_library("electronics/usb_c_breakout")  # receptacle at +x
button = load_library("electronics/tsd_1166_button")  # axis along z, legs on z = 0

# the driving variables, in mm
h = 30.0  # height, outside, along z
wall = 3.0  # thickness of the walls and the floor

# clearances
side_gap = 2.0  # between the holder and the MT3608 / BMS, across y
edge = 2.0  # the MT3608, BMS and button body, in from the +y side
back_gap = 1.0  # the MT3608, from the back wall
board_gap = 2.0  # between the MT3608 and the BMS, along x
usb_gap = 1.0  # at least, between the holder and the USB-C board
plug_clearance = 0.5  # all round the USB-C plug in its hole
button_clearance = 0.3  # all round the button in its hole
button_lift = 1.0  # the button body's underside above the MT3608's top

# the holder, from its size
hb = holder.result.toCompound().BoundingBox()
holder_length, holder_breadth = hb.xlen, hb.ylen

b = holder_breadth + side_gap + boost.width + edge  # breadth, outside
l = 2 * wall + holder_length + usb_gap + usbc.length  # length, outside
back_inside = -l / 2 + wall
front_inside = l / 2 - wall

holder_dx = back_inside - hb.xmin  # its own origin, in the box
holder_dy = -b / 2 - hb.ymin  # flush with the -y side
holder_dz = wall - hb.zmin  # on the floor
assert hb.zlen < h - wall, "the holder is taller than the space inside"

boost_x = back_inside + back_gap + boost.length / 2
boost_y = b / 2 - edge - boost.width / 2
boost_z = wall
bms_x = boost_x + boost.length / 2 + board_gap + bms.length / 2
bms_y = boost_y
bms_z = wall
assert bms_x + bms.length / 2 < front_inside - usbc.length, "the BMS runs into the USB-C board"

usbc_x = front_inside - usbc.length / 2  # its mouth against the front wall
usbc_y = 0.0
usbc_z = wall
usbc_axis = usbc_z + usbc.usb_axis_z  # the plug hole's centre height
usbc_w = 8.25  # USB-C plug shell width
usbc_h = 2.4  # USB-C plug shell height

button_y = b / 2 - edge - button.body / 2
button_z = boost_z + boost.height + button_lift + button.body / 2  # the button's axis
button_hole = button.cap_d + 2 * button_clearance
assert button_z + button.body / 2 < h - 6.0, "the button body reaches the lid's lip"

channel = (
    cq.Workplane("XY", origin=(0, 0, wall))
    .box(l - 2 * wall, b, h - wall, centered=(True, True, False))
)
result = cq.Workplane("XY").box(l, b, h, centered=(True, True, False)).cut(channel)

usbc_hole = (
    cq.Workplane("YZ", origin=(front_inside, usbc_y, usbc_axis))
    .slot2D(usbc_w + 2 * plug_clearance, usbc_h + 2 * plug_clearance)
    .extrude(wall)
)
button_bore = (
    cq.Workplane("YZ", origin=(-l / 2, button_y, button_z))
    .circle(button_hole / 2)
    .extrude(wall)
)
result = result.cut(usbc_hole).cut(button_bore)

regions = {
    "rim": result.faces(">Z"),  # the tops of the two end walls, where the lid sits
    "bottom": result.faces("<Z"),
    "usbc_hole": result.faces().filter(  # the USB-C hole's sides: two flats, two rounded ends
        lambda f: front_inside + 1e-6 < f.Center().x < l / 2 - 1e-6
        and abs(f.Center().y - usbc_y) < usbc_w and abs(f.Center().z - usbc_axis) < usbc_h),
    "button_hole": result.faces("%CYLINDER").filter(lambda f: f.Center().x < 0),
}

if "show_object" in globals():  # CQ-editor (load_library runs under the CAD tool only)
    show_object(result, name="part")
