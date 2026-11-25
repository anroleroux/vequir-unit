"""LS1, assembled.

The LS1: the base with a bought single 18650 holder (power/holder_18650_1s,
wire leads) and its cell glued on the floor against the back wall along
the -y side, the single-cell BMS strip on the cell. Along the +y side a
Pico 2 W stands on its side, 4 mm clear of the button, screwed to the
base's four posts with M1.2 x 6 countersunk screws, the light sensor's
range resistors (R7 to R10) standing out of its back from pins 3 to 6;
behind it the MT3608 boost
board stands on its side in two slotted posts, 4 mm clear of the TP4056,
close to the holder. At the front, the horizontal USB-C
breakout stands on low supports with its front in the front wall's
pocket, held down by the USB clamp (LS1/usb_clamp) and two M1.2 x 6
countersunk screws. Right behind it the wiring board (LS1/wiring_board: the
buzzer, the DS18B20, the transistor, resistors and capacitor packed toward
+y on a perfboard, and the 10-pin box header J2 at its -y edge, its face
against the lid's -y skirt) stands up, its parts facing the front wall and
the buzzer at the top. Behind that the TP4056 charger stands across the
box, its parts facing backwards. Both boards stand in slots in the floor,
held at the top by the board clamp (LS1/board_clamp), screwed with an
M1.2 x 6 countersunk screw to the pillar between them. Behind the TP4056,
D3, D2 and D1 (1N5822) lie across the box one above the other in the
base's three-hole diode pillar, their leads straight and short, their -y
ends 4 mm off the lid. R6 is
soldered inline at the LED stick's data input; R2 stands between the
button's legs, not connected. The TSD-1166 LED push button goes through
the back wall. The lid is seated on top, fastened by four M1.2 x 6
countersunk screws through the end walls into its corner blocks; the
WS2812 8 x 1 stick sits in a shallow pocket inside its +y skirt on two
rests, centred along the side, each LED in its window, unscrewed for now,
with the phototransistor above its middle and an IR LED above each end
LED, turned 10 degrees outward, their domes out through the skirt;
a shroud inside its -y skirt covers J2's top and sides. The bought-in parts
come from vequir-standard.

The base and the lid come from their own scripts through load_part, the
rest through load_library, so the model follows any change to them.

The summary's interference lists each screw against what it is screwed into
(the base's posts and pillars, and the lid's pillars and blocks): a screw's 1.2 mm
shank forming its thread in a 0.95 mm tap hole, as intended, and marked as
a thread.

Assumptions where the description is silent:
- the button is turned so its button points out through the back wall
  (-x), its legs into the box;
- D3, D2 and D1 lie across the box, cathodes toward +y: each the diode with
  straight leads cut to 3 mm (diode.straight), turned a quarter turn about
  z (its x to +y);
- R6 lies along x as it is (the inline resistor is modelled along x); R2 is
  turned a quarter turn about y, so it stands along z; the range resistors a
  quarter turn about z, along y; the IR LEDs and the
  phototransistor a quarter turn about x, their domes (+z) to +y, and the
  IR LEDs then 10 degrees about z, away from the phototransistor;
- the wiring board is turned 120 degrees about (-1, 1, -1): its x to -y, its
  y to -z (row 0, the buzzer's, at the top), its parts' side to +x;
- the board clamp is modelled in place, so it is added as it is; its screw
  stands up, head on top, flush;
- the TP4056 stands turned 120 degrees about (-1, -1, 1): its x (its USB-C
  end) to +y, its y to -z, its z (its parts' side) to -x;
- the stick and the Pico are turned a quarter turn about x so their parts
  face +y (their -y edges at the top); the MT3608 the other way, its parts
  facing -y toward the holder, its VIN end at +x;
- wires, solder and glue are not modelled.
"""
import math

import cadquery as cq

base = load_part("base")  # floor and end walls at +-x, standing on z = 0; the layout
lid = load_part("lid")  # modelled as installed: skirts stand on z = 0
holder = load_library("power/holder_18650_1s")
cell = load_library("power/cell_18650")  # standing up: negative end on z = 0
ir_led = load_library("electronics/led_ir_5mm")  # flange's underside on z = 0, dome toward +z
photo = load_library("electronics/phototransistor_5mm")
boost = load_library("power/mt3608_boost")
bms = load_library("power/bms_1s_3a")
charger = load_library("power/tp4056_charger")
wiring = load_part("wiring_board")  # the perfboard and its parts, standing on z = 0
board_screw = load_library("hardware/m1_2x6_countersunk")
usbc = load_library("electronics/usb_c_breakout")
button = load_library("electronics/tsd_1166_button")
stick = load_library("electronics/ws2812_stick_8")
pico = load_library("electronics/pico_2w")
clamp = load_part("usb_clamp")  # its underside on z = 0
board_clamp = load_part("board_clamp")  # modelled in place
diode = load_library("electronics/diode_1n5822")  # straight leads: body on z = 0, along x, cathode at +x
inline = load_library("electronics/resistor_025w_inline")  # along x, centred
screw = load_library("hardware/m1_2x6_countersunk")  # standing up: tip on z = 0

board_green = cq.Color(0.15, 0.45, 0.30)
board_blue = cq.Color(0.15, 0.30, 0.60)
black = cq.Color(0.10, 0.10, 0.10)
steel = cq.Color(0.70, 0.70, 0.72)
x_axis, y_axis = cq.Vector(1, 0, 0), cq.Vector(0, 1, 0)


def at(x, y, z, axis=None, angle=0):
    if axis is None:
        return cq.Location((x, y, z))
    return cq.Location(cq.Vector(x, y, z), axis, angle)


result = (
    cq.Assembly(name="LS1")
    .add(base.result, name="base", color=cq.Color(0.36, 0.56, 0.78))
    .add(holder.result, name="holder_18650_1s",
         loc=at(base.holder_dx, base.holder_dy, base.holder_dz), color=cq.Color(0.10, 0.10, 0.10))
    # the cell laid along +x in it (a quarter turn about y takes its +z to +x)
    .add(cell.result, name="cell_18650", loc=at(base.cell_x0, base.holder_dy, base.cell_z, y_axis, 90),
         color=cq.Color(0.88, 0.56, 0.24))
    .add(bms.result, name="bms_1s_3a", loc=at(base.bms_x, base.bms_y, base.bms_z), color=board_green)
    .add(charger.result, name="tp4056_charger",
         loc=at(base.charger_x, base.charger_y, base.charger_z, cq.Vector(-1, -1, 1), 120),
         color=board_blue)
    # standing up, its parts facing +x, row 0 at the top
    .add(wiring.result, name="wiring_board",
         loc=at(base.wb_back_x, base.wb_y, base.wb_zc, cq.Vector(-1, 1, -1), 120))
    # a quarter turn about x: -90 takes the board's +z (its parts) to +y, +90 to -y
    .add(pico.result, name="pico_2w",
         loc=at(base.pico_x, base.pico_y, base.pico_z, x_axis, -90), color=board_green)
    .add(boost.result, name="mt3608_boost",
         loc=at(base.mt_x, base.mt_y, base.mt_z, x_axis, 90), color=board_blue)
    .add(usbc.result, name="usb_c_breakout",
         loc=at(base.usbc_x, base.usbc_y, base.usbc_z), color=board_blue)
    # a quarter turn about y takes the button's +z (its button) to -x
    .add(button.result, name="tsd_1166_button",
         loc=at(base.button_x, base.button_y, base.button_z, y_axis, -90), color=black)
    .add(clamp.result, name="usb_clamp", loc=at(base.clamp_x, 0, base.clamp_z),
         color=cq.Color(0.36, 0.56, 0.78))
    .add(stick.result, name="ws2812_stick_8",
         loc=at(base.stick_x, base.stick_y, base.stick_z, x_axis, -90), color=black)
)

# the Pico's screws: heads on its parts' side (+y), down in its 2.1 mm holes
pico_head = base.pico_y + pico.pcb_t + base.head_out(pico.mount_hole)  # the heads' tops
for i, (x, z) in enumerate(base.pico_holes, start=1):
    result.add(screw.result, name=f"pico_screw_{i}",
               loc=at(x, pico_head - screw.length, z, x_axis, -90), color=steel)

# the board clamp over the pillar between the boards, and its screw
result.add(board_clamp.result, name="board_clamp", color=cq.Color(0.36, 0.56, 0.78))
result.add(board_screw.result, name="board_clamp_screw",
           loc=at(base.pillar_x, base.pillar_y, base.bc_screw_top - board_screw.length), color=steel)

# D3, D2 and D1 in the diode pillar, one above the other, leads straight
straight = diode.straight(base.diode_lead)
for name, z in (("d3_1n5822", base.d3_z), ("d2_1n5822", base.d2_z), ("d1_1n5822", base.d1_z)):
    result.add(straight, name=name, loc=at(base.diodes_x, base.diodes_y, z, cq.Vector(0, 0, 1), 90),
               color=black)

# R6 inline at the stick; R2 standing up between the button's legs
inline_tan = cq.Color(0.80, 0.70, 0.50)
result.add(inline.result, name="r6_inline", loc=at(base.r6_x, base.r6_y, base.r6_z), color=inline_tan)
result.add(inline.result, name="r2_inline", loc=at(base.r2_x, base.r2_y, base.r2_z, y_axis, 90),
           color=inline_tan)

# the light sensor's range resistors on the Pico's pins 3 to 6, standing -y
# out of its back (a quarter turn about z takes the resistor's x to y)
for ref, (x, z) in base.pico_res_at.items():
    result.add(inline.result, name=f"{ref.lower()}_inline", loc=at(x, base.pico_res_y, z, cq.Vector(0, 0, 1), 90),
               color=inline_tan)

# the phototransistor above the stick and an IR LED above each end LED,
# through the lid's +y skirt: a quarter turn about x takes each one's dome
# (+z) to +y; each IR LED is then turned about z, away from the
# phototransistor, its flange's top centred at (x, ir_face_y, ir_z)
clear_lens = cq.Color(0.75, 0.80, 0.90)
for i, (x, angle) in enumerate(zip(base.ir_xs, base.ir_angles), start=1):
    a = math.radians(angle)
    axis = cq.Vector(-math.sin(a), math.cos(a), 0)
    origin = cq.Vector(x, base.ir_face_y, base.ir_z) - axis * ir_led.flange_t  # the flange's underside
    shape = (ir_led.result.rotate((0, 0, 0), (1, 0, 0), -90).rotate((0, 0, 0), (0, 0, 1), angle)
             .translate(origin))
    result.add(shape, name=f"ir_led_{i}", color=cq.Color(0.30, 0.30, 0.45))
result.add(photo.result, name="phototransistor", loc=at(base.photo_x, base.lens_y, base.photo_z, x_axis, -90),
           color=clear_lens)

# the lid's screws, through the end walls from outside, heads flush
for i, (x, y, z) in enumerate(base.lid_screws, start=1):
    side = 1 if x > 0 else -1
    result.add(board_screw.result, name=f"lid_screw_{i}",
               loc=at(x - side * board_screw.length, y, z, y_axis, side * 90), color=steel)

for i, (x, y) in enumerate(base.clamp_holes, start=1):
    result.add(board_screw.result, name=f"clamp_screw_{i}",
               loc=at(x, y, base.clamp_screw_top - board_screw.length), color=steel)

result.add(lid.result, name="lid", loc=at(0, 0, base.h - lid.seat_height),
           color=cq.Color(0.40, 0.68, 0.45))

regions = {}

if "show_object" in globals():  # CQ-editor (load_part runs under the CAD tool only)
    show_object(result, name="LS1")
