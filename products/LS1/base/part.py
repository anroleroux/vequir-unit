"""LS1 base box.

A floor and two end walls, open at the top and along both long sides, like
the PB6 base but for one cell. A bought single-cell 18650 holder with
wire leads (power/holder_18650_1s) and its cell are glued on the floor
against the back wall along the -y side, with the single-cell BMS strip
on the cell. Along the +y side, behind the WS2812 stick on the lid, a
Pico 2 W stands on its side, 4 mm clear of the button, screwed with four
M1.2 x 6 countersunk screws to four posts; behind it the MT3608 boost
board stands on its side in two slotted posts, 4 mm clear of
the TP4056 and close to the battery holder. At the front, the horizontal USB-C
breakout stands on low supports with its front in a pocket in the front
wall, 0.4 mm from the outside, held down by a clamp (LS1/usb_clamp) screwed
to two posts over its receptacle. Right behind it the wiring board (a
perfboard with the buzzer, the DS18B20, the transistor, resistors,
capacitor and a 10-pin box header) stands up, its parts facing the front
wall and the buzzer at the top, its parts packed toward +y and the box
header at its -y edge, opening toward -y against the lid; behind that the
TP4056 charger stands across the box, its parts facing backwards. Each
board's bottom edge stands in a slot in the floor, and a clamp
(LS1/board_clamp), screwed with an M1.2 x 6 countersunk screw to a pillar
rising between the two boards, holds both top edges in two slots. Behind
the TP4056, D3, D2 and D1 lie across the box one above the other in a
pillar with three holes, their leads straight, their -y ends 4 mm off the
lid. The front wall has a USB-C plug hole and
round vent holes; the TSD-1166 LED push button goes through a round hole in
the back wall. Each end wall has two countersunk holes near its ends for
the M1.2 screws that fasten the lid's blocks from outside. The box is sized from the parts, so it follows a
change to any of them.

Assumptions where the description is silent:
- l, b and h are outside dimensions, the floor is as thick as the walls,
  wall = 3 and h = 30 mm; l and b follow from the parts below;
- the holder's negative (spring) end is against the back wall and its -y
  side flush with the box's -y side; it is glued, so the floor has no
  pillars for it; the BMS lies on the top of the cell, centred on it;
- across the breadth, from the +y side in: the stick in its pocket in the
  lid (its board 0.4 mm into the 1 mm pocket on 0.6 mm rests), 1 mm clear,
  the Pico with its parts facing +y, its posts behind it, then the MT3608
  with its board's back at least 2.1 mm behind the Pico's (so its slotted
  posts clear the Pico), its parts facing -y; the breadth is that with
  1 mm to the holder, or more if the wiring board's box header
  (J2, 9 mm deep, against the -y side) needs it to clear the USB-C board's
  side by 0.5 mm: it does, so b is 39.2 mm; the MT3608 then sits with its
  parts 0.5 mm off the holder's side, which leaves 5.5 mm between its
  board and the Pico's;
- the Pico's lower long edge is 1 mm above the floor; its USB end (-x) is
  4 mm clear of the button's leg tips; its four posts are 3 mm along x and
  5.5 mm deep behind it (the +x ones only 5.2 mm, stopping 0.3 mm short of
  the MT3608's board), up to 1.5 mm above its upper holes, with M1.2 tap
  holes (0.95 mm, 5 mm deep, for the 4.7 mm of an M1.2 x 6 screw past the
  board) in line with its mounting holes; the stick is centred along the
  box (x = 0);
- the MT3608 stands on the floor, its +x end 4 mm clear of the TP4056's
  parts; each of its two
  posts is 11.5 mm tall and holds one end of the board in a vertical slot
  (the board's 1.6 mm plus 0.2 mm), 1.2 mm deep, with 1.5 mm walls, clear of
  the corner holes; the board slides in from the top;
- the wiring board stands 1 mm above the floor, its 12 columns across the
  breadth and its 9 rows up the height (row 0, the buzzer's, at the top),
  its parts side 1 mm plus its tallest low part (C1) behind the USB-C
  board; across, it sits so the face of its box header (J2), past its -y
  edge, touches the lid's -y skirt (0.33 mm off centre); J2 clears the
  USB-C board's side by 0.36 mm;
- each board's slot is a rail along its bottom edge, as long as the board,
  with a groove 0.1 mm wider than the board each side and 1.0 mm deep,
  1.2 mm walls either side; the TP4056's bottom edge is 1.2 mm off the
  floor; the boards slide in from the top;
- the clamp's pillar is 3 mm square, centred between the two boards' backs
  (6.5 mm apart: room for the buzzer's pins) and behind the wiring board's
  column 9, which is kept empty (so it clears the leads' ends either side),
  up to 0.5 mm under the wiring board's top edge, with an M1.2 tap hole
  (0.95 mm) 4.5 mm deep from its top; the clamp (LS1/board_clamp) is 4 mm
  wide, its bar 2 mm thick on the pillar, its two slots taking 1.0 mm of
  each board's top edge;
- D3, D2 and D1 (1N5822) lie across the box, one above the other, 1 mm
  behind the TP4056's parts, cathodes toward +y (D2 and D3 are joined, to
  the MT3608's VIN+), their leads straight and cut to 3 mm, the ends of
  their -y leads 4 mm off the lid's -y skirt; the pillar is
  a block 7 mm long (shorter than the bodies, so the leads are free) with a
  bore 0.1 mm round each body and 1.2 mm walls under, round and between
  them; the bodies push in;
- R6 (inline, its leads cut to 3 mm) is in line with the LED stick, 0.5 mm
  past its -x end, at its board's mid-plane, in the stick's pocket in the
  lid, on the data wire into the stick's DIN pad at that end;
- the 5 mm phototransistor (Micro Robotics BP0334) sits above the stick's
  middle, its flange 0.3 mm clear of the stick's pocket, and a 5 mm IR LED
  above each of the stick's end LEDs, centred on it, at the same height,
  turned 10 degrees about z away from the phototransistor; each has its
  flange against the inside of the lid's +y skirt (only the outer rim of
  an IR LED's tilted flange touches), its dome out through a hole (about
  4.6 mm proud), its leads to be bent and wired at the flange; R2 (inline) stands up along z between the
  button's two rows of legs, centred on its axis and halfway along the
  legs, touching nothing (its wires are not modelled);
- the USB-C breakout's underside is 2 mm above the floor; its front 2.6 mm
  sits in a pocket in the front wall (0.2 mm clearance round the board and
  over the receptacle), so its mouth is 0.4 mm from the wall's outside, and
  the plug hole (the plug's 8.25 x 2.4 mm shell with 0.5 mm clearance,
  round-ended) goes through that 0.4 mm; the pocket's floor and two 2 mm
  square supports under the board's sides, at its middle, carry it;
- the clamp's two posts are 3.5 mm square, 0.5 mm beside the board, up to
  the receptacle's top, centred under the clamp, which lies 0.3 mm behind
  the wall; each has an M1.2 tap hole 4.5 mm deep;
- the TP4056 stands across the box, 6.5 mm behind the wiring board's
  back, its parts facing -x, its USB-C end (IN+ and IN-) toward +y, its OUT
  end toward -y, its lower edge 1.2 mm off the floor in its slot;
- the vents are round holes, 2.4 mm across at 3.6 mm pitch, across the
  front wall 2 mm in from its sides, from 1 mm above the USB-C pocket up to
  2 mm under the rim, 1 mm clear of the lid's blocks;
- the lid's four blocks (in the lid) are 4 mm along x, 5 mm across and 6 mm
  deep, 0.2 mm inside the end walls; each end wall has two M1.2 clearance
  holes (1.3 mm) through it in line with the blocks' centres, countersunk
  on the outside for flush M1.2 x 6 heads;
- the button's hole is its 10 mm button plus 0.3 mm all round, its axis
  15 mm up and 8 mm in from the +y side; its body rests against the inside
  of the back wall, so its button stands 2 mm proud;
- the box is centred on x and y and stands on z = 0, l along x (+x the
  front), b along y; corners are sharp.
"""
import math

import cadquery as cq

holder = load_library("power/holder_18650_1s")  # the bought holder, wire leads; the cell goes in it
cell = load_library("power/cell_18650")  # standing up: axis along z, negative end on z = 0
boost = load_library("power/mt3608_boost")  # 36 x 17 boost board
bms = load_library("power/bms_1s_3a")  # 30.3 x 3.7 protection strip
charger = load_library("power/tp4056_charger")  # 28 x 17, USB-C at +x
usbc = load_library("electronics/usb_c_breakout")  # receptacle at +x
button = load_library("electronics/tsd_1166_button")  # axis along z, legs on z = 0
pico = load_library("electronics/pico_2w")  # USB at -x, underside on z = 0
stick = load_library("electronics/ws2812_stick_8")  # on the lid's +y skirt
wiring = load_part("../wiring_board")  # the perfboard and its parts, standing on z = 0
diode = load_library("electronics/diode_1n5822")  # formed: body on z = 0, leads below, anode at -x
inline = load_library("electronics/resistor_025w_inline")  # along x, centred
ir_led = load_library("electronics/led_ir_5mm")  # flange's underside on z = 0, dome toward +z
photo = load_library("electronics/phototransistor_5mm")  # the same package
screw = load_library("hardware/m1_2x6_countersunk")  # for the Pico
board_screw = load_library("hardware/m1_2x6_countersunk")  # for the wiring board and the clamp

# the driving variables, in mm
h = 30.0  # height, outside, along z
wall = 3.0  # thickness of the walls and the floor

# clearances and sizes
gap = 1.0  # between neighbouring parts
tap_drill = 0.95  # M1.2 x 0.25
tap_depth = 5.0  # the Pico's posts: past the 4.73 mm of screw behind the board
stick_inset = 1.0  # the stick's pocket in the lid's +y skirt, deep
stick_rest = 0.6  # its two rests in the pocket: the board's LED side off the pocket's floor
pico_gap = 4.0  # the Pico's -x end (its USB), clear of the button's legs
mt_holder_gap = 0.5  # the MT3608's parts, clear of the holder's side
post_mt_gap = 0.3  # the Pico's +x posts' backs, clear of the MT3608's board
lens_gap = 0.3  # each LED's and the phototransistor's flange, clear of the stick's pocket
ir_tilt = 10.0  # degrees: each IR LED turned away from the phototransistor
lens_clearance = 0.1  # radial, round each one's body in its hole in the lid
clamp_lip_t = 1.2  # the USB clamp's lip behind the receptacle, along x
clamp_lip_gap = 0.2  # between the lip and the receptacle's back
clamp_tongue_side = 1.0  # the clamp's tongue, past the receptacle's sides
clamp_lip_above = 0.3  # the lip's bottom, above the USB-C board's top
mt_gap = 4.0  # the MT3608's +x end, clear of the TP4056's parts
diode_lid_gap = 4.0  # the diodes' -y lead ends, clear of the lid's -y skirt
header_usb_gap = 0.5  # J2's back, clear of the USB-C board's side
stick_z = 18.0  # the stick's centre line, above the bottom
pico_lift = 1.0  # the Pico's lower edge above the floor
post = 3.0  # the Pico's posts, along x
post_d = 5.5  # and behind its underside, along y: the tap hole plus 0.5 mm
post_above = 1.5  # above the Pico's upper holes
mt_behind = 2.1  # the MT3608's back face, behind the Pico's
slot_clearance = 0.2  # round the MT3608's board in its slots
slot_engagement = 1.2  # of each board end in its slot
slot_wall = 1.5
slot_post_h = 11.5  # the MT3608's posts, clear of D1
button_clearance = 0.3  # all round the button in its hole
button_z = 15.0  # the button's axis
button_in = 2.0  # its body, in from the +y side
between_boards = 6.5  # the wiring board's back to the TP4056's back: the buzzer's pins and the pillar
board_lift = 1.0  # the wiring board's bottom edge, above the floor
charger_lift = 1.2  # the TP4056's bottom edge, above the floor
rail_wall = 1.2  # each side of a board's slot
rail_clearance = 0.1  # each side of a board in its slot or the clamp's
rail_engage = 1.0  # each board's bottom edge in its slot, and its top edge in the clamp
pillar = 3.0  # the clamp's pillar between the boards, square
bc_w = 4.0  # the board clamp, across (along y)
bc_t = 2.0  # its bar's thickness, over the pillar
bc_under = 0.5  # the bar's underside, below the wiring board's top edge
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
usb_end_gap = 0.2  # past the TP4056's receptacle, which stands proud of its USB end
holder_wall = 1.2  # the diode holder, round and between its bores
holder_len = 7.0  # its length along the diodes (shorter than their bodies)
bore_clearance = 0.1  # radial, round each diode body
diode_lead = 3.0  # each diode's straight leads, cut short
vent_d = 2.4  # round vent holes
vent_pitch = 3.6
vent_in = 2.0  # from the wall's sides
vent_gap = 1.0  # from the parts and the blocks round them
vent_top = 2.0  # under the rim
lid_block_t = 4.0  # the lid's blocks: along x
lid_block_w = 5.0  # across, from the skirt in
lid_block_depth = 6.0  # under the plate
lid_clearance = 0.2  # between each block and its end wall
lid_hole = 1.3  # M1.2 clearance, through the end walls


# the screw heads' rise above a board: a 90 degree head sits down in a plain
# hole until its cone is as wide as the hole; the short edge at dk stays above
def head_out(hole, s=screw):
    return s.edge_height + (s.head_diameter - hole) / 2


# across the breadth, from the +y side in (relative to b / 2)
stick_back_in = stick.pcb_t - (stick_inset - stick_rest)  # the stick's back face, partly in its pocket
pico_top_in = stick_back_in + gap  # the Pico's parts' tops
pico_under_in = pico_top_in + pico.height  # the Pico's underside
mt_under_in = pico_under_in + mt_behind  # the MT3608's underside (its back)
mt_parts_in = mt_under_in + boost.height  # its trimmer's top
holder_edge_in = mt_parts_in + gap  # the holder's +y side

# the holder, from its size (the cell lies within it)
hb = holder.result.val().BoundingBox()
holder_length, holder_breadth = hb.xlen, hb.ylen

# the front zone, in front of the holder, from the front wall back: the USB-C
# board (partly in the wall), the wiring board standing up (its parts facing
# the wall) on its posts, the TP4056 turned across the box in its corner
# pillars, and D2 and D3 across the box; each as a distance from the wall's inside
wb = wiring.board  # the perfboard: length (across the breadth), width (its height, standing)
low_parts = max(wiring.capacitor.height, wiring.resistor.height)  # its parts beside the USB-C board
usb_rear_in = usbc.length - (wall - usb_skin)
wb_face_in = usb_rear_in + gap + low_parts  # the wiring board's parts side
wb_back_in = wb_face_in + wb.thickness
tp_back_in = wb_back_in + between_boards  # the TP4056's back (solder side), standing
tp_parts_in = tp_back_in + charger.pcb_t + charger.height - charger.pcb_t
holder_d = diode.body_d + 2 * (bore_clearance + holder_wall)  # the diode holder, along x
holder_front_in = tp_parts_in + gap
front_zone_length = holder_front_in + holder_d + gap
assert wiring.buzzer.body_bottom - wb.thickness < between_boards - rail_clearance - rail_wall, \
    "the buzzer's pins reach the TP4056's slot"

# breadth, outside: what the +y side's layout needs, or (if more) room for
# the wiring board's box header (J2, against the -y side) beside the USB-C board
header_depth = wiring.header.depth
b = max(holder_breadth + holder_edge_in, 2 * (header_depth + usbc.width / 2 + header_usb_gap))
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
bms_z = holder_dz + holder.axis_height + cell.diameter / 2
# the cell in the holder, laid along +x: its negative end on the spring
cell_x0 = holder_dx + holder.cell_x0
cell_z = holder_dz + holder.axis_height
assert abs(holder.cell_diameter - cell.diameter) < 1e-6, "the holder is for another cell"

# the wiring board standing up behind the USB-C board, its parts facing +x
# (the wall), its rows up the height with row 0 (the buzzer's) at the top and
# its columns across: turned 120 degrees about (-1, 1, -1), which takes its x
# to -y, its y to -z and its z (its parts' side) to +x
wb_back_x = front_inside - wb_back_in  # its underside's plane
# across, J2's opening (past the board's -y edge) touches the lid's -y skirt:
# its row A, at the board's own x, is front_off behind the face
header = wiring.header
wb_y = -b / 2 + header.front_off + wb.header_centre[0]
wb_bottom = wall + board_lift
wb_zc = wb_bottom + wb.width / 2  # its centre's height
wb_top = wb_bottom + wb.width
header_z0 = wb_zc - header.length / 2  # J2's ends, up the height
header_z1 = wb_zc + header.length / 2
header_x1 = wb_back_x + wb.thickness + header.height  # its top, toward the front wall
assert abs(wb_y) + wb.length / 2 < b / 2, "the wiring board is wider than the box"
assert wb_top < h, "the wiring board is taller than the box"
assert header_z0 > wb_bottom + rail_engage, "J2 runs into the wiring board's slot"

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
# its tongue back over the receptacle, past its back, and the lip down behind it
usb_shell_back = usbc_front - usbc.usb_d
clamp_lip_x1 = usb_shell_back - clamp_lip_gap
clamp_lip_x0 = clamp_lip_x1 - clamp_lip_t
clamp_tongue_w = usbc.usb_w + 2 * clamp_tongue_side
clamp_lip_bottom = usbc_z + usbc.pcb_t + clamp_lip_above
assert clamp_tongue_w / 2 < clamp_post_y - clamp_post / 2, "the clamp's tongue runs into its posts"
assert header_x1 < usbc_x - usbc.length / 2 or wb_y - wb.header_centre[0] + header.back_y < -usbc.width / 2, \
    "J2 runs into the USB-C board"

# the TP4056 standing up behind the wiring board's posts, its parts facing -x
# (backwards), its length across the box with its USB-C end (IN+ and IN-)
# toward +y and its OUT end toward -y: turned 120 degrees about (-1, -1, 1),
# which takes its x to +y, its y to -z and its z (its parts' side) to -x
charger_x = front_inside - tp_back_in  # its underside's (solder side's) plane
charger_y = 0.0
charger_bottom = wall + charger_lift  # its lower edge, in its slot
charger_z = charger_bottom + charger.width / 2  # its centre's height
charger_top = charger_bottom + charger.width
charger_face = charger_x - charger.pcb_t  # its parts' side
assert charger.length / 2 + charger.usb_proud + usb_end_gap < b / 2, \
    "the TP4056 is too long to stand across"

# the two boards' slots in the floor, and the clamp's pillar between them,
# behind the wiring board's column 9 (kept empty) and clear of its leads
wb_slot_x = (wb_back_x - rail_clearance, wb_back_x + wb.thickness + rail_clearance)
tp_slot_x = (charger_face - rail_clearance, charger_x + rail_clearance)
pillar_x = (charger_x + wb_back_x) / 2
pillar_y = wb_y - wb.at(9, 0)[0]
bc_bottom = wb_top - bc_under  # the clamp's bar: its underside, over the pillar
bc_top = bc_bottom + bc_t
bc_screw_top = bc_top  # its screw's head, flush
assert bc_top < h, "the board clamp reaches the lid"
assert charger_top - rail_engage > charger_bottom, "the TP4056 is too short for its slot and clamp"
assert (pillar_x - pillar / 2 > charger_x + rail_clearance
        and pillar_x + pillar / 2 < wb_back_x - (wiring.resistor.below - wb.thickness)), \
    "the clamp's pillar runs into a board or the wiring board's leads"

# D3, D2 and D1 behind it, one above the other in the diode pillar, across
# the box, cathodes toward +y, their leads straight
holder_x = front_inside - holder_front_in - holder_d / 2
diode_bore = diode.body_d + 2 * bore_clearance
d3_axis = wall + holder_wall + diode_bore / 2
d2_axis = d3_axis + diode_bore + holder_wall
d1_axis = d2_axis + diode_bore + holder_wall
diode_axes = [d3_axis, d2_axis, d1_axis]
holder_top = d1_axis + diode_bore / 2 + holder_wall
diodes_x = holder_x
diodes_y = -b / 2 + diode_lid_gap + diode.body_length / 2 + diode_lead  # their -y lead ends 4 mm off the lid
d3_z, d2_z, d1_z = (z - diode.body_d / 2 for z in diode_axes)  # each one's own z = 0: its body's bottom
assert holder_x - holder_d / 2 >= front_zone - 1e-6, "the diode holder runs into the holder"
assert holder_top < h, "the diode pillar reaches the lid"

# the button through the back wall: its leg tips, turned to point +x
button_x = back_inside + button.body_top

# the Pico on its side, parts facing +y, its USB (-x) end pico_gap clear of
# the button's legs, and its four posts
pico_mounts = [(sx * pico.mount_x / 2, sy * pico.mount_y / 2) for sx in (-1, 1) for sy in (-1, 1)]
pico_x = button_x + pico_gap + pico.usb_overhang + pico.length / 2
pico_y = b / 2 - pico_under_in  # its underside's plane
pico_z = wall + pico_lift + pico.width / 2  # its centre line
pico_holes = [(pico_x + x, pico_z - y) for x, y in pico_mounts]  # (x, z), turned about x
post_xs = [pico_x + sx * pico.mount_x / 2 for sx in (-1, 1)]
post_top = pico_z + pico.mount_y / 2 + post_above

# the MT3608 on its side, parts facing -y, in its slotted posts, its +x end
# mt_gap clear of the TP4056's parts
mt_x = charger_face - (charger.height - charger.pcb_t) - mt_gap - boost.length / 2
mt_y = holder_edge + mt_holder_gap + boost.height  # its underside's plane (the board's back)
# the Pico's +x posts stop short of the MT3608's board, which is behind them
post_ds = [post_d, min(post_d, pico_y - mt_y - post_mt_gap)]
assert post_ds[1] >= tap_depth, "no room behind the Pico for its +x posts' tap holes"
mt_z = wall + boost.width / 2  # standing on the floor
slot_w = boost.pcb_t + slot_clearance
slot_y = mt_y - boost.pcb_t / 2  # the slot's centre line
mt_post_len = slot_engagement + slot_clearance / 2 + slot_wall  # along x
mt_post_w = slot_w + 2 * slot_wall  # along y
mt_post_xs = [mt_x + s * (boost.length / 2 - slot_engagement + mt_post_len / 2) for s in (-1, 1)]
assert slot_y + mt_post_w / 2 <= pico_y - 0.5, "the MT3608's posts touch the Pico"
assert mt_y - boost.height >= holder_edge + mt_holder_gap - 1e-6, "the MT3608 runs into the holder"
assert (diodes_y + diode.body_length / 2 + diode_lead < slot_y - mt_post_w / 2 - 0.5
        or mt_post_xs[1] + mt_post_len / 2 < holder_x - holder_d / 2), "the MT3608 runs into the diodes"

# the stick on the lid, centred along the box's +y side, in its pocket
stick_x = 0.0
stick_y = b / 2 - stick_back_in  # its underside's plane
stick_holes = [(stick_x + x, stick_z - stick.cap_y) for x in stick.hole_xs]  # (x, z), turned: its rests
assert stick_x + stick.length / 2 < charger_face - (charger.height - charger.pcb_t) - gap, \
    "the LED stick reaches the TP4056"


# the lid's screws: through each end wall into the lid's blocks
lid_screws = [(sx * l / 2, sy * (b / 2 - lid_block_w / 2), h - lid_block_depth / 2)
              for sx in (-1, 1) for sy in (-1, 1)]
lid_screw_head = head_out(lid_hole, board_screw)  # the countersink's depth for a flush head

# the button through the back wall
button_y = b / 2 - button_in - button.body / 2
button_hole = button.cap_d + 2 * button_clearance

# R6 inline at the LED stick's -x end, along x, in the stick's pocket; R2
# standing up between the button's two rows of legs, clear of them and of
# its body
r6_x = stick_x - stick.length / 2 - 0.5 - inline.length / 2
r6_y = stick_y + stick.pcb_t / 2  # the stick's board, mid-plane
r6_z = stick_z
# the stick's pocket in the lid (the lid cuts it): two rectangles, (x0, x1,
# z0, z1), the stick's and R6's past its -x end
stick_pocket_clearance = 0.2  # round the stick and R6, in their pocket in the lid
c_ = stick_pocket_clearance
stick_pocket = [
    (stick_x - stick.length / 2 - c_, stick_x + stick.length / 2 + c_,
     stick_z - stick.width / 2 - c_, stick_z + stick.width / 2 + c_),
    (r6_x - inline.length / 2 - c_, stick_x - stick.length / 2,
     r6_z - inline.body_d / 2 - c_, r6_z + inline.body_d / 2 + c_),
]
# the phototransistor above the stick's middle, and an IR LED above each of
# the stick's end LEDs at the same height, each through a hole in the lid's
# +y skirt, its flange against the skirt's inside and its dome out; the IR
# LEDs are turned ir_tilt about z, away from the phototransistor
photo_x = stick_x
photo_z = stick_pocket[0][3] + lens_gap + photo.flange_d / 2
lens_y = b / 2 - ir_led.flange_t  # the phototransistor's own z = 0 (its flange's underside), turned to +y
ir_xs = [stick_x + stick.led_xs[0], stick_x + stick.led_xs[-1]]
ir_z = photo_z
ir_angles = [ir_tilt if x < photo_x else -ir_tilt for x in ir_xs]  # about z: + turns the dome (+y) toward -x
# each IR LED's flange top (its centre) sits so its rim just reaches the skirt
ir_face_y = b / 2 - ir_led.flange_d / 2 * math.sin(math.radians(ir_tilt))
assert abs(ir_xs[0] - photo_x) > (ir_led.flange_d + photo.flange_d) / 2 + lens_gap, \
    "an IR LED runs into the phototransistor"
assert photo_z + photo.flange_d / 2 < h, "the phototransistor reaches the lid's plate"
assert lens_y - ir_led.lead > b / 2 - pico_top_in, "the phototransistor's leads reach the Pico"
r2_x = button_x - button.leg_length / 2
r2_y = button_y
r2_z = button_z
assert inline.body_d / 2 < button.leg_rows / 2 - button.leg[1] / 2 - 0.5, "R2 touches the button's legs"
assert inline.body_d / 2 < button.leg_length / 2 - 0.5, "R2 touches the button's body"
assert r2_z - inline.length / 2 > wall, "R2 reaches the floor"

# the vents: round holes across the front wall, from the USB-C pocket up, clear of the blocks
vent_bands = [(pocket_top + vent_gap, h - vent_top)]
vent_n = math.floor((b - 2 * vent_in - vent_d) / vent_pitch) + 1
vent_ys = [(i - (vent_n - 1) / 2) * vent_pitch for i in range(vent_n)]
vent_holes = []
for z0, z1 in vent_bands:
    rows = math.floor((z1 - z0 - vent_d) / vent_pitch) + 1
    for j in range(max(rows, 0)):
        z = (z0 + z1) / 2 + (j - (rows - 1) / 2) * vent_pitch
        for y in vent_ys:
            by_block = (abs(y) + vent_d / 2 > b / 2 - lid_block_w - vent_gap
                        and z + vent_d / 2 > h - lid_block_depth - vent_gap)
            if not by_block:
                vent_holes.append((y, z))

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
vents = (cq.Workplane("YZ", origin=(front_inside, 0, 0)).pushPoints(vent_holes)
         .circle(vent_d / 2).extrude(wall))
# the lid's screw holes, countersunk on the outside
lid_holes = None
for x, y, z in lid_screws:
    side = 1 if x > 0 else -1
    sink_r = board_screw.head_diameter / 2 + 0.05
    cone_h = sink_r - lid_hole / 2
    edge = board_screw.edge_height
    # "YZ" extrudes toward +x: start each cut at its -x face
    hole = (cq.Workplane("YZ", origin=(x - wall if side > 0 else x, y, z))
            .circle(lid_hole / 2).extrude(wall))
    bore = (cq.Workplane("YZ", origin=(x - edge if side > 0 else x, y, z))
            .circle(sink_r).extrude(edge))
    cone = cq.Solid.makeCone(lid_hole / 2, sink_r, cone_h,
                             cq.Vector(x - side * (edge + cone_h), y, z),
                             cq.Vector(side, 0, 0))
    cut = hole.union(bore).union(cq.Workplane("XY").add(cone))
    lid_holes = cut if lid_holes is None else lid_holes.union(cut)
button_bore = (
    cq.Workplane("YZ", origin=(-l / 2, button_y, button_z))
    .circle(button_hole / 2)
    .extrude(wall)
)
result = result.cut(pocket).cut(usbc_hole).cut(vents).cut(button_bore).cut(lid_holes)

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
# the boards' slots: a rail along each board's bottom edge, with a groove
# for the edge; the boards slide in from the top
def rail(x0, x1, y_mid, y_len, floor_z):
    block = (cq.Workplane("XY", origin=(x0 - rail_wall, y_mid - y_len / 2, wall))
             .box(x1 - x0 + 2 * rail_wall, y_len, floor_z + rail_engage - wall, centered=False))
    groove = (cq.Workplane("XY", origin=(x0, y_mid - y_len / 2, floor_z))
              .box(x1 - x0, y_len, rail_engage, centered=False))
    return block.cut(groove)


board_slots = (rail(*wb_slot_x, wb_y, wb.length, wb_bottom)
               .union(rail(*tp_slot_x, charger_y, charger.length, charger_bottom)))
# the clamp's pillar between the boards, and its tap hole from the top
clamp_pillar = (cq.Workplane("XY", origin=(pillar_x, pillar_y, wall))
                .rect(pillar, pillar).extrude(bc_bottom - wall))
pillar_tap = (cq.Workplane("XY", origin=(pillar_x, pillar_y, bc_bottom - long_tap))
              .circle(tap_drill / 2).extrude(long_tap))
# the diode holder: a block with a bore for each diode's body, one above the other
diode_holder = (
    cq.Workplane("XY", origin=(holder_x, diodes_y, wall))
    .box(holder_d, holder_len, holder_top - wall, centered=(True, True, False))
)
for z in diode_axes:
    diode_holder = diode_holder.cut(
        cq.Workplane("XZ", origin=(0, diodes_y + holder_len / 2, 0)).center(holder_x, z)
        .circle(diode_bore / 2).extrude(holder_len))
# the Pico's posts, behind its underside, and their tap holes along -y
pico_posts = None
for x, d in zip(post_xs, post_ds):
    one = (cq.Workplane("XY", origin=(x, pico_y - d / 2, wall))
           .rect(post, d).extrude(post_top - wall))
    pico_posts = one if pico_posts is None else pico_posts.union(one)
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
result = (result.union(supports).union(clamp_posts).cut(clamp_taps)
          .union(board_slots).union(diode_holder)
          .union(pico_posts).cut(pico_taps).union(mt_posts.cut(mt_slots))
          .union(clamp_pillar).cut(pillar_tap))

regions = {
    "rim": result.faces(">Z"),  # the tops of the two end walls, where the lid sits
    "bottom": result.faces("<Z"),
    "usbc_hole": result.faces().filter(  # the USB-C hole's sides: two flats, two rounded ends
        lambda f: usbc_front + 1e-6 < f.Center().x < l / 2 - 1e-6
        and abs(f.Center().y - usbc_y) < usbc_w and abs(f.Center().z - usbc_axis) < usbc_h),
    "usbc_pocket": result.faces("%PLANE").filter(  # its back face, 0.4 mm from the outside
        lambda f: f.normalAt().x < -0.999 and abs(f.Center().x - usbc_front) < 1e-6),
    "vents": result.faces("%CYLINDER").filter(  # the round vent holes
        lambda f: abs(f.BoundingBox().ylen - vent_d) < 1e-3 and abs(f.BoundingBox().xlen - wall) < 1e-3
        and f.Center().x > 0),
    "lid_screw_holes": result.faces("%CYLINDER").filter(  # through the end walls
        lambda f: abs(f.BoundingBox().ylen - lid_hole) < 1e-3),
    "button_hole": result.faces("%CYLINDER").filter(
        lambda f: f.Center().x < -l / 2 + wall and abs(f.BoundingBox().ylen - button_hole) < 1e-3),
    "pico_post_faces": result.faces("%PLANE").filter(  # where the Pico's underside rests
        lambda f: f.normalAt().y > 0.999 and abs(f.Center().y - pico_y) < 1e-6),
    "pico_tap_holes": result.faces("%CYLINDER").filter(
        lambda f: abs(f.BoundingBox().xlen - tap_drill) < 1e-3
        and abs(f.BoundingBox().ylen - tap_depth) < 1e-3),
    "long_tap_holes": result.faces("%CYLINDER").filter(  # the USB clamp's and the board clamp's
        lambda f: abs(f.BoundingBox().zlen - long_tap) < 1e-3),
    "board_slots": result.faces("%PLANE").filter(  # the grooves' floors, where the boards' edges rest
        lambda f: f.normalAt().z > 0.999 and (abs(f.Center().z - wb_bottom) < 1e-6
                                             or abs(f.Center().z - charger_bottom) < 1e-6)),
    "diode_bores": result.faces("%CYLINDER").filter(
        lambda f: abs(f.BoundingBox().xlen - diode_bore) < 1e-3 and abs(f.BoundingBox().ylen - holder_len) < 1e-3),
    "mt_slots": result.faces("%PLANE").filter(  # the slots' bottoms, where the board's ends go
        lambda f: abs(abs(f.normalAt().x) - 1) < 1e-6
        and abs(abs(f.Center().x - mt_x) - (boost.length / 2 + slot_clearance / 2)) < 1e-6),
}

if "show_object" in globals():  # CQ-editor (load_library runs under the CAD tool only)
    show_object(result, name="part")
