"""LS1 base box.

A floor and two end walls, open at the top and along both long sides, like
the PB6 base but for one cell. A single 18650 holder from the parts library
(battery_holders/single_18650_holder) is glued on the floor against the back
wall along the -y side, with the single-cell BMS strip on its cell.
Along the +y side, behind the WS2812 stick on the lid, a Pico 2 W stands on
its side, screwed with four M1.2 x 3 countersunk screws to four posts rising
from the floor, and behind it the MT3608 boost board stands on its side in
two slotted posts. In front of the holder, the wiring board (a perfboard
with the buzzer, the DS18B20, the diodes, resistors, capacitor and
transistor) is screwed to four tall pillars with M1.2 x 6 countersunk
screws, in the upper half of the box. Under it, the TP4056 charger lies in
four corner pillars on the floor, and in front of that the horizontal USB-C
breakout stands on low supports with its front in a pocket in the front
wall, 0.4 mm from the outside, held down by a clamp (LS1/usb_clamp) screwed
to two posts over its receptacle. The front wall has a USB-C plug hole and
two rows of vent slots; the TSD-1166 LED push button goes through a round
hole in the back wall. The box is sized from the parts, so it follows a
change to any of them.

Assumptions where the description is silent:
- l, b and h are outside dimensions, the floor is as thick as the walls,
  wall = 3 and h = 30 mm; l and b follow from the parts below;
- the holder's back end (the clips' lugs) is against the back wall and its
  -y side flush with the box's -y side; it is glued, so the floor has no
  pillars for it; the BMS lies on the top of the cell, centred on it;
- across the breadth, from the +y side in: the stick on the lid (its
  pillars 0.6 mm, its board, its screw heads), 1 mm clear, the Pico with its
  parts facing +y, its posts behind it, then the MT3608 with its board's
  back 2.1 mm behind the Pico's (so its slotted posts clear the Pico), its
  parts facing -y, and 1 mm clear of the holder;
- the Pico's lower long edge is 1 mm above the floor and its four posts are
  3 x 3 mm, up to 1.5 mm above its upper holes, with M1.2 tap holes
  (0.95 mm, 2.5 mm deep) in line with its mounting holes; the Pico and the
  stick are centred on the same x, the Pico's +x posts 1 mm behind the
  front zone (which starts 1 mm in front of the holder);
- the MT3608 stands on the floor, centred on the Pico's x; each of its two
  posts is 12 mm tall and holds one end of the board in a vertical slot
  (the board's 1.6 mm plus 0.2 mm), 1.2 mm deep, with 1.5 mm walls, clear of
  the corner holes; the board slides in from the top;
- the wiring board's underside is at mid-height inside the box (the upper
  half), its 14 columns across the breadth (turned a quarter turn about z),
  centred across it, its front edge 0.5 mm behind the front wall and its
  back edge at least 0.5 mm into the front zone; it stands on four 4 mm
  square pillars from the floor, one under each drilled corner hole, each
  with an M1.2 tap hole (0.95 mm) 4.5 mm deep;
- the USB-C breakout's underside is 2 mm above the floor; its front 2.6 mm
  sits in a pocket in the front wall (0.2 mm clearance round the board and
  over the receptacle), so its mouth is 0.4 mm from the wall's outside, and
  the plug hole (the plug's 8.25 x 2.4 mm shell with 0.5 mm clearance,
  round-ended) goes through that 0.4 mm; the pocket's floor and two 2 mm
  square supports under the board's sides, at its middle, carry it;
- the clamp's two posts are 3.5 mm square, 0.5 mm beside the board, up to
  the receptacle's top, centred under the clamp, which lies 0.3 mm behind
  the wall; each has an M1.2 tap hole 4.5 mm deep;
- the TP4056 lies with its USB-C end (IN+ and IN-) forward, its receptacle
  1 mm behind the USB-C breakout, centred across the box; each corner
  pillar is a 1.5 mm ledge under 1.9 mm of the board's corner, with 1.2 mm
  walls round the corner outside its edges, 0.8 mm above its top, 0.1 mm
  clear of its edges; it is pressed in (or glued);
- the vents are vertical slots 1.6 mm wide at 3.2 mm pitch across the front
  wall, 2 mm in from its sides, in two rows: between the USB-C pocket and
  the wiring board, and between the wiring board and the lid's lip, each
  1 mm clear of them;
- the button's hole is its 10 mm button plus 0.3 mm all round, its axis
  15 mm up and 8 mm in from the +y side; its body rests against the inside
  of the back wall, so its button stands 2 mm proud;
- the box is centred on x and y and stands on z = 0, l along x (+x the
  front), b along y; corners are sharp.
"""
import math

import cadquery as cq

holder = load_library("battery_holders/single_18650_holder")  # the cell in its holder
boost = load_library("power/mt3608_boost")  # 36 x 17 boost board
bms = load_library("power/bms_1s_3a")  # 30.3 x 3.7 protection strip
charger = load_library("power/tp4056_charger")  # 28 x 17, USB-C at +x
usbc = load_library("electronics/usb_c_breakout")  # receptacle at +x
button = load_library("electronics/tsd_1166_button")  # axis along z, legs on z = 0
pico = load_library("electronics/pico_2w")  # USB at -x, underside on z = 0
stick = load_library("electronics/ws2812_stick_8")  # on the lid's +y skirt
wiring = load_part("../wiring_board")  # the perfboard and its parts, standing on z = 0
screw = load_library("hardware/m1_2x3_countersunk")  # for the Pico and the stick
board_screw = load_library("hardware/m1_2x6_countersunk")  # for the wiring board and the clamp

# the driving variables, in mm
h = 30.0  # height, outside, along z
wall = 3.0  # thickness of the walls and the floor

# clearances and sizes
gap = 1.0  # between neighbouring parts
tap_drill = 0.95  # M1.2 x 0.25
tap_depth = 2.5  # the Pico's posts
stick_standoff = 0.6  # the stick's pillars on the lid: its board off the skirt
stick_z = 18.0  # the stick's centre line, above the bottom
pico_lift = 1.0  # the Pico's lower edge above the floor
post = 3.0  # the Pico's posts, square
post_above = 1.5  # above the Pico's upper holes
mt_behind = 2.1  # the MT3608's back face, behind the Pico's
slot_clearance = 0.2  # round the MT3608's board in its slots
slot_engagement = 1.2  # of each board end in its slot
slot_wall = 1.5
slot_post_h = 12.0  # the MT3608's posts
button_clearance = 0.3  # all round the button in its hole
button_z = 15.0  # the button's axis
button_in = 2.0  # its body, in from the +y side
board_pillar = 4.0  # the wiring board's pillars, square
board_wall_gap = 0.5  # the wiring board's edges, from the front wall and the front zone
long_tap = 4.5  # the M1.2 x 6 screws' tap holes, from the pillar's top
usb_skin = 0.4  # the front wall left in front of the USB-C board
usb_raise = 2.0  # the USB-C board's underside, above the floor
pocket_clearance = 0.2  # round the USB-C board in its pocket
usb_support = 2.0  # its two supports behind the wall, square
plug_clearance = 0.5  # all round the USB-C plug in its hole
usbc_w = 8.25  # USB-C plug shell width
usbc_h = 2.4  # USB-C plug shell height
clamp_w = 4.0  # the clamp's width, along x
clamp_t = 2.5  # its thickness
clamp_behind = 0.3  # behind the front wall
clamp_post = 3.5  # its posts, square
clamp_post_gap = 0.5  # beside the USB-C board
ledge = 1.5  # the TP4056's ledges, above the floor
corner_under = 2.0  # each ledge, under the board's corner
corner_wall = 1.2  # the walls round its corners
corner_above = 0.8  # above its top
corner_clearance = 0.1  # round its edges
vent_w = 1.6  # vent slot width
vent_pitch = 3.2
vent_in = 2.0  # from the wall's sides
vent_gap = 1.0  # above and below each row
lip_depth = 6.0  # the lid's lips reach this far below the rim


# the screw heads' rise above a board: a 90 degree head sits down in a plain
# hole until its cone is as wide as the hole; the short edge at dk stays above
def head_out(hole, s=screw):
    return s.edge_height + (s.head_diameter - hole) / 2


# across the breadth, from the +y side in (relative to b / 2)
stick_back_in = stick_standoff + stick.pcb_t  # the stick's back face
pico_top_in = stick_back_in + head_out(stick.hole) + gap  # the Pico's parts' tops
pico_under_in = pico_top_in + pico.height  # the Pico's underside
mt_under_in = pico_under_in + mt_behind  # the MT3608's underside (its back)
mt_parts_in = mt_under_in + boost.height  # its trimmer's top
holder_edge_in = mt_parts_in + gap  # the holder's +y side

# the holder, from its size
hb = holder.result.toCompound().BoundingBox()
holder_length, holder_breadth = hb.xlen, hb.ylen

# the front zone, in front of the holder: the wiring board above; below it,
# from the front wall back, the USB-C board (partly in the wall), the TP4056
# and its corner walls
wb = wiring.board  # the perfboard: length (across the breadth), width (along x)
board_zone = wb.width + 2 * board_wall_gap
usb_zone = (usbc.length - (wall - usb_skin) + gap + charger.length + charger.usb_proud
            + corner_wall + gap)
front_zone_length = max(board_zone, usb_zone)

b = holder_breadth + holder_edge_in  # breadth, outside
l = 2 * wall + holder_length + gap + front_zone_length  # length, outside
back_inside = -l / 2 + wall
front_inside = l / 2 - wall
front_zone = back_inside + holder_length + gap  # where the holder's room ends

holder_dx = back_inside - hb.xmin  # its own origin, in the box
holder_dy = -b / 2 - hb.ymin  # flush with the -y side
holder_dz = wall - hb.zmin  # on the floor
holder_edge = -b / 2 + holder_breadth
assert hb.zlen < h - wall, "the holder is taller than the space inside"

# the BMS on the cell, centred on the holder
bms_x = holder_dx
bms_y = holder_dy  # the cell's axis
bms_z = holder_dz + holder.axis_height + holder.cell.diameter / 2

# the wiring board, raised, turned so its columns run across
wb_x = front_inside - board_wall_gap - wb.width / 2
wb_y = 0.0
wb_z = wall + (h - wall) / 2  # its underside: mid-height inside
wb_holes = [(wb_x - y, wb_y + x) for x, y in wb.mount_holes]  # a quarter turn about z
wb_screw_top = wb_z + wb.thickness + head_out(wb.mount_hole, board_screw)
assert wb.length < b, "the wiring board is wider than the box"

# the USB-C board, its front in the wall's pocket
usbc_front = l / 2 - usb_skin
usbc_x = usbc_front - usbc.length / 2
usbc_y = 0.0
usbc_z = wall + usb_raise
usbc_axis = usbc_z + usbc.usb_axis_z  # the plug hole's centre height
usbc_top = usbc_z + usbc.height  # the receptacle's top
pocket_w = usbc.width + 2 * pocket_clearance
pocket_top = usbc_top + pocket_clearance
usbc_supports = [(usbc_x, s * (usbc.width / 2 - usb_support / 2)) for s in (-1, 1)]

# the clamp over the receptacle, and its posts
clamp_x = front_inside - clamp_behind - clamp_w / 2
clamp_post_y = usbc.width / 2 + clamp_post_gap + clamp_post / 2
clamp_holes = [(clamp_x, s * clamp_post_y) for s in (-1, 1)]
clamp_z = usbc_top  # its underside, on the receptacle
clamp_screw_top = clamp_z + clamp_t  # flush with its top
assert clamp_x - clamp_w / 2 > usbc_front - usbc.usb_d, "the clamp is not over the receptacle"

# the TP4056 behind it, on its corner pillars
charger_front = usbc_front - usbc.length - gap  # its receptacle's mouth
charger_x = charger_front - charger.usb_proud - charger.length / 2
charger_y = 0.0
charger_z = wall + ledge
charger_corners = [(charger_x + sx * charger.length / 2, charger_y + sy * charger.width / 2)
                   for sx in (-1, 1) for sy in (-1, 1)]
assert charger_x - charger.length / 2 - corner_wall >= front_zone - 1e-6, "the TP4056 runs into the holder"

# the Pico on its side, parts facing +y, and its posts
pico_mounts = [(sx * pico.mount_x / 2, sy * pico.mount_y / 2) for sx in (-1, 1) for sy in (-1, 1)]
pico_x = front_zone - gap - (pico.mount_x / 2 + post / 2)
pico_y = b / 2 - pico_under_in  # its underside's plane
pico_z = wall + pico_lift + pico.width / 2  # its centre line
pico_holes = [(pico_x + x, pico_z - y) for x, y in pico_mounts]  # (x, z), turned about x
post_xs = [pico_x + sx * pico.mount_x / 2 for sx in (-1, 1)]
post_top = pico_z + pico.mount_y / 2 + post_above

# the MT3608 on its side, parts facing -y, in its slotted posts
mt_x = pico_x
mt_y = b / 2 - mt_under_in  # its underside's plane (the board's back)
mt_z = wall + boost.width / 2  # standing on the floor
slot_w = boost.pcb_t + slot_clearance
slot_y = mt_y - boost.pcb_t / 2  # the slot's centre line
mt_post_len = slot_engagement + slot_clearance / 2 + slot_wall  # along x
mt_post_w = slot_w + 2 * slot_wall  # along y
mt_post_xs = [mt_x + s * (boost.length / 2 - slot_engagement + mt_post_len / 2) for s in (-1, 1)]
assert slot_y + mt_post_w / 2 <= pico_y - 0.5, "the MT3608's posts touch the Pico"
assert mt_y - boost.height >= holder_edge + gap - 1e-6, "the MT3608 runs into the holder"

# the stick on the lid, centred on the Pico, and its screws
stick_x = pico_x
stick_y = b / 2 - stick_back_in  # its underside's plane
stick_holes = [(stick_x + x, stick_z - stick.cap_y) for x in stick.hole_xs]  # (x, z), turned
assert stick_x + stick.length / 2 < wb_x - wb.width / 2, "the LED stick runs into the wiring board"

# the button through the back wall
button_y = b / 2 - button_in - button.body / 2
button_hole = button.cap_d + 2 * button_clearance
button_x = back_inside + button.body_top  # its leg tips, turned to point +x

# the vents: two rows of slots across the front wall
vent_rows = [(pocket_top + vent_gap, wb_z - vent_gap),
             (wb_z + wb.thickness + vent_gap, h - lip_depth - vent_gap)]
vent_n = math.floor((b - 2 * vent_in - vent_w) / vent_pitch) + 1
vent_ys = [(i - (vent_n - 1) / 2) * vent_pitch for i in range(vent_n)]

channel = (
    cq.Workplane("XY", origin=(0, 0, wall))
    .box(l - 2 * wall, b, h - wall, centered=(True, True, False))
)
result = cq.Workplane("XY").box(l, b, h, centered=(True, True, False)).cut(channel)

# the front wall: the USB-C board's pocket, its plug hole, the vents
pocket = (
    cq.Workplane("XY", origin=(front_inside, usbc_y - pocket_w / 2, usbc_z))
    .box(wall - usb_skin, pocket_w, pocket_top - usbc_z, centered=False)
)
usbc_hole = (
    cq.Workplane("YZ", origin=(usbc_front, usbc_y, usbc_axis))
    .slot2D(usbc_w + 2 * plug_clearance, usbc_h + 2 * plug_clearance)
    .extrude(usb_skin)
)
vents = None
for z0, z1 in vent_rows:
    row = (cq.Workplane("YZ", origin=(front_inside, 0, (z0 + z1) / 2))
           .pushPoints([(y, 0) for y in vent_ys])
           .slot2D(z1 - z0, vent_w, angle=90).extrude(wall))
    vents = row if vents is None else vents.union(row)
button_bore = (
    cq.Workplane("YZ", origin=(-l / 2, button_y, button_z))
    .circle(button_hole / 2)
    .extrude(wall)
)
result = result.cut(pocket).cut(usbc_hole).cut(vents).cut(button_bore)

# the USB-C board's supports, and the clamp's posts with their tap holes
supports = (
    cq.Workplane("XY", origin=(0, 0, wall)).pushPoints(usbc_supports)
    .rect(usb_support, usb_support).extrude(usb_raise)
)
clamp_posts = (
    cq.Workplane("XY", origin=(0, 0, wall)).pushPoints(clamp_holes)
    .rect(clamp_post, clamp_post).extrude(clamp_z - wall)
)
clamp_taps = (
    cq.Workplane("XY", origin=(0, 0, clamp_z - long_tap)).pushPoints(clamp_holes)
    .circle(tap_drill / 2).extrude(long_tap)
)
# the TP4056's corner pillars: blocks round each corner, less the board's room above the ledge
corner = corner_under + corner_wall
corner_blocks = (
    cq.Workplane("XY", origin=(0, 0, wall))
    .pushPoints([(x + (corner / 2 - corner_under) * (1 if x > charger_x else -1),
                  y + (corner / 2 - corner_under) * (1 if y > charger_y else -1))
                 for x, y in charger_corners])
    .rect(corner, corner).extrude(ledge + charger.pcb_t + corner_above)
)
board_room = (
    cq.Workplane("XY", origin=(charger_x, charger_y, charger_z))
    .rect(charger.length + 2 * corner_clearance, charger.width + 2 * corner_clearance)
    .extrude(charger.pcb_t + corner_above)
)
# the Pico's posts, behind its underside, and their tap holes along -y
pico_posts = (
    cq.Workplane("XY", origin=(0, pico_y - post / 2, wall))
    .pushPoints([(x, 0) for x in post_xs])
    .rect(post, post).extrude(post_top - wall)
)
pico_taps = (
    cq.Workplane("XZ", origin=(0, pico_y, 0))  # normal -y: into the posts
    .pushPoints(pico_holes)
    .circle(tap_drill / 2).extrude(tap_depth)
)
# the MT3608's slotted posts
mt_posts = (
    cq.Workplane("XY", origin=(0, slot_y, wall))
    .pushPoints([(x, 0) for x in mt_post_xs])
    .rect(mt_post_len, mt_post_w).extrude(slot_post_h)
)
mt_slots = (
    cq.Workplane("XY", origin=(0, slot_y, wall))
    .pushPoints([(mt_x + s * (boost.length / 2 + slot_clearance / 2 - (slot_engagement + slot_clearance / 2) / 2), 0)
                 for s in (-1, 1)])
    .rect(slot_engagement + slot_clearance / 2, slot_w).extrude(slot_post_h)
)
# the wiring board's pillars and their tap holes
board_pillars = (
    cq.Workplane("XY", origin=(0, 0, wall)).pushPoints(wb_holes)
    .rect(board_pillar, board_pillar).extrude(wb_z - wall)
)
board_taps = (
    cq.Workplane("XY", origin=(0, 0, wb_z - long_tap)).pushPoints(wb_holes)
    .circle(tap_drill / 2).extrude(long_tap)
)
result = (result.union(supports).union(clamp_posts).cut(clamp_taps)
          .union(corner_blocks.cut(board_room))
          .union(pico_posts).cut(pico_taps).union(mt_posts.cut(mt_slots))
          .union(board_pillars).cut(board_taps))

regions = {
    "rim": result.faces(">Z"),  # the tops of the two end walls, where the lid sits
    "bottom": result.faces("<Z"),
    "usbc_hole": result.faces().filter(  # the USB-C hole's sides: two flats, two rounded ends
        lambda f: usbc_front + 1e-6 < f.Center().x < l / 2 - 1e-6
        and abs(f.Center().y - usbc_y) < usbc_w and abs(f.Center().z - usbc_axis) < usbc_h),
    "usbc_pocket": result.faces("%PLANE").filter(  # its back face, 0.4 mm from the outside
        lambda f: f.normalAt().x < -0.999 and abs(f.Center().x - usbc_front) < 1e-6),
    "vents": result.faces("%PLANE").filter(  # the vent slots' flat sides
        lambda f: abs(abs(f.normalAt().y) - 1) < 1e-6 and front_inside + 1e-6 < f.Center().x < l / 2
        and f.Center().z > pocket_top),
    "button_hole": result.faces("%CYLINDER").filter(lambda f: f.Center().x < -l / 2 + wall),
    "pico_post_faces": result.faces("%PLANE").filter(  # where the Pico's underside rests
        lambda f: f.normalAt().y > 0.999 and abs(f.Center().y - pico_y) < 1e-6),
    "pico_tap_holes": result.faces("%CYLINDER").filter(
        lambda f: abs(f.BoundingBox().xlen - tap_drill) < 1e-3
        and abs(f.BoundingBox().ylen - tap_depth) < 1e-3),
    "long_tap_holes": result.faces("%CYLINDER").filter(  # the wiring board's and the clamp's
        lambda f: abs(f.BoundingBox().zlen - long_tap) < 1e-3),
    "charger_ledges": result.faces("+Z").filter(
        lambda f: abs(f.Center().z - charger_z) < 1e-6),
    "mt_slots": result.faces("%PLANE").filter(  # the slots' bottoms, where the board's ends go
        lambda f: abs(abs(f.normalAt().x) - 1) < 1e-6
        and abs(abs(f.Center().x - mt_x) - (boost.length / 2 + slot_clearance / 2)) < 1e-6),
}

if "show_object" in globals():  # CQ-editor (load_library runs under the CAD tool only)
    show_object(result, name="part")
