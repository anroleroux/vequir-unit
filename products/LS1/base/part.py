"""LS1 base box.

A floor and two end walls, open at the top and along both long sides, like
the PB6 base but for one cell. A single 18650 holder from the parts library
(battery_holders/single_18650_holder) is glued on the floor against the back
wall along the -y side, with the TP4056 charger module lying across its
front end and the single-cell BMS strip on its cell behind that.
Along the +y side, behind the WS2812 stick on the lid, a Pico 2 W stands on
its side, screwed with four M1.2 x 3 countersunk screws to four posts rising
from the floor, and behind it the MT3608 boost board stands on its side in
two slotted posts. In front of the holder the wiring board (a perfboard
with the diodes, resistors and transistor) is screwed to four pillars with
M1.2 x 6 countersunk screws, and in front of it a horizontal USB-C breakout
sits on two pillars, its receptacle behind a USB-C plug hole in the front
wall; the
TSD-1166 LED push button goes through a round hole in the back wall; the
active buzzer stands on the floor beside the button, and the bare DS18B20
stands in the open air at the front. The box is sized from the parts, so it
follows a change to any of them.

Assumptions where the description is silent:
- l, b and h are outside dimensions, the floor is as thick as the walls,
  wall = 3 and h = 30 mm; l and b follow from the parts below;
- the holder's back end (the clips' lugs) is against the back wall and its
  -y side flush with the box's -y side; it is glued, so the floor has no
  pillars for it;
- across the breadth, from the +y side in: the stick on the lid (its
  pillars 0.6 mm, its board, its screw heads), 1 mm clear, the Pico with its
  parts facing +y, its posts behind it, then the MT3608 with its board's
  back 2.1 mm behind the Pico's (so its slotted posts clear the Pico), its
  parts facing -y, and 1 mm clear of the holder;
- the Pico's lower long edge is 1 mm above the floor and its four posts are
  3 x 3 mm, up to 1.5 mm above its upper holes, with M1.2 tap holes
  (0.95 mm, 2.5 mm deep) in line with its mounting holes; the Pico and the
  stick are centred on the same x, the Pico's +x posts 1 mm behind the
  wiring board;
- the MT3608 stands on the floor, centred on the Pico's x; each of its two
  posts is 12 mm tall and holds one end of the board in a vertical slot
  (the board's 1.6 mm plus 0.2 mm), 1.2 mm deep, with 1.5 mm walls, clear of
  the corner holes; the board slides in from the top;
- the TP4056 module lies on the holder's rims, its front end flush with the
  holder body's front, its USB-C end (IN+ and IN-) forward, toward the USB-C
  breakout; its own USB-C port is not used; the BMS lies on the top of the
  cell behind it, along it, 1 mm clear (both glued or held by their leads);
- the wiring board lies 1 mm in front of the holder, its 14 columns across
  the breadth (turned a quarter turn about z), centred across it, on four
  2.5 mm square pillars 3 mm tall (clear of its leads, which stand 1.4 mm out
  underneath), one under each drilled corner hole, each with an M1.2 tap
  hole (0.95 mm) 4.5 mm deep; the USB-C breakout is 1 mm in front of it;
- the USB-C breakout's holes are larger (3.2 mm) than an M1.2 screw's head,
  so its two pillars (5 mm round, 2 mm tall) each carry a 3.0 mm peg
  through the board's hole, to glue or melt over, instead of a screw;
- the button's hole is its 10 mm button plus 0.3 mm all round, its axis
  15 mm up and 8 mm in from the +y side; its body rests against the inside
  of the back wall, so its button stands 2 mm proud;
- the buzzer stands on its pins on the floor, 0.5 mm in front of the
  button's legs, 1 mm clear of the holder; no sound hole in the box yet;
- the DS18B20 stands on its leads on the floor in front of the holder, at
  -y beside the USB-C board, in the air inside the box;
- the box is centred on x and y and stands on z = 0, l along x (+x the
  front), b along y; corners are sharp.
"""
import cadquery as cq

holder = load_library("battery_holders/single_18650_holder")  # the cell in its holder
boost = load_library("power/mt3608_boost")  # 36 x 17 boost board
bms = load_library("power/bms_1s_3a")  # 30.3 x 3.7 protection strip
charger = load_library("power/tp4056_charger")  # 28 x 17, USB-C at +x
wiring = load_part("../wiring_board")  # the perfboard and its parts, standing on z = 0
usbc = load_library("electronics/usb_c_breakout")  # receptacle at +x
button = load_library("electronics/tsd_1166_button")  # axis along z, legs on z = 0
pico = load_library("electronics/pico_2w")  # USB at -x, underside on z = 0
stick = load_library("electronics/ws2812_stick_8")  # on the lid's +y skirt
buzzer = load_library("electronics/buzzer_12x9")  # pins' tips on z = 0
sensor = load_library("electronics/ds18b20")  # TO-92, leads' tips on z = 0
screw = load_library("hardware/m1_2x3_countersunk")  # for the Pico and the stick
board_screw = load_library("hardware/m1_2x6_countersunk")  # for the wiring board

# the driving variables, in mm
h = 30.0  # height, outside, along z
wall = 3.0  # thickness of the walls and the floor

# clearances and sizes
gap = 1.0  # between neighbouring parts
tap_drill = 0.95  # M1.2 x 0.25
tap_depth = 2.5
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
pillar_d = 5.0  # the USB-C board's pillars
pillar_h = 2.0
peg_d = 3.0  # through the board's 3.2 mm holes
button_clearance = 0.3  # all round the button in its hole
button_z = 15.0  # the button's axis
button_in = 2.0  # its body, in from the +y side
plug_clearance = 0.5  # all round the USB-C plug in its hole
usbc_w = 8.25  # USB-C plug shell width
usbc_h = 2.4  # USB-C plug shell height
board_pillar = 2.5  # the wiring board's pillars, square
board_pillar_h = 3.0  # clear of the leads under the board
board_tap_depth = 4.5  # from the pillars' tops

# the screw heads' rise above a board: a 90 degree head sits down in a plain
# hole until its cone is as wide as the hole; the short edge at dk stays above
def head_out(hole):
    return screw.edge_height + (screw.head_diameter - hole) / 2

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

b = holder_breadth + holder_edge_in  # breadth, outside
wb = wiring.board  # the perfboard: length (across the breadth), width (along x)
l = 2 * wall + holder_length + gap + wb.width + gap + usbc.length  # length, outside
back_inside = -l / 2 + wall
front_inside = l / 2 - wall

holder_dx = back_inside - hb.xmin  # its own origin, in the box
holder_dy = -b / 2 - hb.ymin  # flush with the -y side
holder_dz = wall - hb.zmin  # on the floor
holder_edge = -b / 2 + holder_breadth
assert hb.zlen < h - wall, "the holder is taller than the space inside"

# the TP4056 on the holder's rims at its front end, the BMS on the cell behind it
holder_front = holder_dx + holder.body.length / 2  # the body's front, its outer end wall
charger_x = holder_front - charger.length / 2
charger_y = holder_dy  # centred on the holder
charger_z = holder_dz + holder.body.height  # on the rims
bms_x = charger_x - charger.length / 2 - gap - bms.length / 2
bms_y = holder_dy  # the cell's axis
bms_z = holder_dz + holder.axis_height + holder.cell.diameter / 2
assert charger.width <= holder.body.width, "the TP4056 is wider than the holder"

# the wiring board in front of the holder, turned so its columns run across
front_zone = back_inside + holder_length + gap  # where the holder's room ends
wb_x = front_zone + wb.width / 2
wb_y = 0.0
wb_z = wall + board_pillar_h  # its underside
wb_holes = [(wb_x - y, wb_y + x) for x, y in wb.mount_holes]  # a quarter turn about z
wb_screw_top = wb_z + wb.thickness + board_screw.edge_height + (board_screw.head_diameter - wb.mount_hole) / 2
assert wb.length < b, "the wiring board is wider than the box"

# the USB-C board on its pillars, mouth against the front wall
usbc_x = front_inside - usbc.length / 2
usbc_y = 0.0
usbc_z = wall + pillar_h
usbc_axis = usbc_z + usbc.usb_axis_z  # the plug hole's centre height
usbc_pegs = [(usbc_x + x, usbc_y + y) for x, y in usbc.mount_holes]
assert usbc_x - usbc.length / 2 >= wb_x + wb.width / 2 + gap - 1e-6, "the USB-C board runs into the wiring board"

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

# the button through the back wall, the buzzer beside it, the sensor in front
button_y = b / 2 - button_in - button.body / 2
button_hole = button.cap_d + 2 * button_clearance
button_x = back_inside + button.body_top  # its leg tips, turned to point +x
buzzer_x = button_x + 0.5 + buzzer.diameter / 2
buzzer_y = holder_edge + gap + buzzer.diameter / 2
buzzer_z = wall
assert buzzer_x + buzzer.diameter / 2 < pico_x - pico.length / 2 - 1.3, "the buzzer runs into the Pico"
sensor_x = usbc_x
sensor_y = (-b / 2 + usbc_y - usbc.width / 2) / 2  # between the -y side and the USB-C board
sensor_z = wall

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

# the USB-C board's pillars and pegs
pillars = (
    cq.Workplane("XY", origin=(0, 0, wall)).pushPoints(usbc_pegs)
    .circle(pillar_d / 2).extrude(pillar_h)
    .faces(">Z").workplane().pushPoints(usbc_pegs)
    .circle(peg_d / 2).extrude(usbc.pcb_t)
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
    .rect(board_pillar, board_pillar).extrude(board_pillar_h)
)
board_taps = (
    cq.Workplane("XY", origin=(0, 0, wb_z - board_tap_depth)).pushPoints(wb_holes)
    .circle(tap_drill / 2).extrude(board_tap_depth)
)
result = (result.union(pillars).union(pico_posts).cut(pico_taps).union(mt_posts.cut(mt_slots))
          .union(board_pillars).cut(board_taps))

regions = {
    "rim": result.faces(">Z"),  # the tops of the two end walls, where the lid sits
    "bottom": result.faces("<Z"),
    "usbc_hole": result.faces().filter(  # the USB-C hole's sides: two flats, two rounded ends
        lambda f: front_inside + 1e-6 < f.Center().x < l / 2 - 1e-6
        and abs(f.Center().y - usbc_y) < usbc_w and abs(f.Center().z - usbc_axis) < usbc_h),
    "button_hole": result.faces("%CYLINDER").filter(lambda f: f.Center().x < -l / 2 + wall),
    "usbc_pegs": result.faces("%CYLINDER").filter(
        lambda f: abs(f.BoundingBox().xlen - peg_d) < 1e-3),
    "pico_post_faces": result.faces("%PLANE").filter(  # where the Pico's underside rests
        lambda f: f.normalAt().y > 0.999 and abs(f.Center().y - pico_y) < 1e-6),
    "pico_tap_holes": result.faces("%CYLINDER").filter(
        lambda f: abs(f.BoundingBox().xlen - tap_drill) < 1e-3
        and abs(f.BoundingBox().ylen - tap_depth) < 1e-3),
    "board_tap_holes": result.faces("%CYLINDER").filter(
        lambda f: abs(f.BoundingBox().zlen - board_tap_depth) < 1e-3),
    "mt_slots": result.faces("%PLANE").filter(  # the slots' bottoms, where the board's ends go
        lambda f: abs(abs(f.normalAt().x) - 1) < 1e-6
        and abs(abs(f.Center().x - mt_x) - (boost.length / 2 + slot_clearance / 2)) < 1e-6),
}

if "show_object" in globals():  # CQ-editor (load_library runs under the CAD tool only)
    show_object(result, name="part")
