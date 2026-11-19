"""LS1, assembled.

The LS1: the base with a single 18650 holder and its cell (vequir-power's
battery_holders/single_18650_holder) glued on the floor against the back
wall along the -y side, the single-cell BMS strip on the cell. Along the +y
side a Pico 2 W stands on its side, screwed to the base's four posts with
M1.2 x 3 countersunk screws, and behind it the MT3608 boost board stands on
its side in two slotted posts. In front of the holder, on the floor, the
TP4056 charger sits in four corner pillars, and in front of it the
horizontal USB-C breakout stands on low supports with its front in the
front wall's pocket, held down by the USB clamp (LS1/usb_clamp) and two
M1.2 x 6 countersunk screws. D2 and D3 (1N5822) lie across the floor
behind the TP4056, leads up for the wires, and D1 is soldered by its anode
lead into the MT3608's VOUT+ hole. R6 is soldered inline at the LED stick's
data input, and R2 on the button's LED+ leg. Above them, in the upper half, the wiring
board (LS1/wiring_board: the buzzer, the DS18B20, the diodes, resistors,
capacitor and transistor on a perfboard) is screwed to four tall pillars
with M1.2 x 6 countersunk screws. The TSD-1166 LED push button goes through
the back wall. The lid is seated on top, fastened by four M1.2 x 6
countersunk screws through the end walls into its corner blocks, and the WS2812 8 x 1 stick is
screwed to two pillars inside its +y skirt with M1.2 x 3 countersunk
screws, each LED in its window, in front of the Pico. The bought-in parts
come from vequir-standard.

The base and the lid come from their own scripts through load_part, the
rest through load_library, so the model follows any change to them.

The summary's interference lists each screw against what it is screwed into
(the base's posts and pillars, and the lid's pillars): a screw's 1.2 mm
shank forming its thread in a 0.95 mm tap hole, as intended, and marked as
a thread.

Assumptions where the description is silent:
- the button is turned so its button points out through the back wall
  (-x), its legs into the box;
- D1 lies on the MT3608's parts side, its anode lead through the VOUT+ hole,
  its body out past the board's VOUT end (-x), its cathode lead free for the
  VSYS wire: the formed diode turned half a turn about (0, 1, -1), which takes
  its x to -x, its y to -z and its z (away from the board) to -y;
- D3 and D2 are the formed diode upside down, across the box: D3 turned half
  a turn about (1, 1, 0) (its x to +y, its z to -z), D2 about (1, -1, 0)
  (its x to -y), so both anodes point outward and the cathodes meet;
- R6 and R2 lie along x as they are (the inline resistor is modelled along x);
- the stick and the Pico are turned a quarter turn about x so their parts
  face +y (their -y edges at the top); the MT3608 the other way, its parts
  facing -y toward the holder, its VIN end at +x;
- wires, solder and glue are not modelled.
"""
import cadquery as cq

base = load_part("base")  # floor and end walls at +-x, standing on z = 0; the layout
lid = load_part("lid")  # modelled as installed: skirts stand on z = 0
holder = load_library("battery_holders/single_18650_holder")
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
diode = load_library("electronics/diode_1n5822")  # formed: the board's top on z = 0, anode at -x
inline = load_library("electronics/resistor_025w_inline")  # along x, centred
screw = load_library("hardware/m1_2x3_countersunk")  # standing up: tip on z = 0

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
    .add(holder.result, name="single_18650_holder",
         loc=at(base.holder_dx, base.holder_dy, base.holder_dz))
    .add(bms.result, name="bms_1s_3a", loc=at(base.bms_x, base.bms_y, base.bms_z), color=board_green)
    .add(charger.result, name="tp4056_charger",
         loc=at(base.charger_x, base.charger_y, base.charger_z), color=board_blue)
    # a quarter turn about z: the board's columns run across the breadth
    .add(wiring.result, name="wiring_board",
         loc=at(base.wb_x, base.wb_y, base.wb_z, cq.Vector(0, 0, 1), 90))
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

# the stick's screws: heads on its back (-y), through its 2.0 mm holes into the pillars
stick_head = base.stick_y - base.head_out(stick.hole)
for i, (x, z) in enumerate(base.stick_holes, start=1):
    result.add(screw.result, name=f"stick_screw_{i}",
               loc=at(x, stick_head + screw.length, z, x_axis, 90), color=steel)

for i, (x, y) in enumerate(base.wb_holes, start=1):
    result.add(board_screw.result, name=f"board_screw_{i}",
               loc=at(x, y, base.wb_screw_top - board_screw.length), color=steel)

# D2 and D3 across the floor behind the TP4056
result.add(diode.result, name="d3_1n5822",
           loc=at(base.diodes_x, base.d3_y, base.diodes_z, cq.Vector(1, 1, 0), 180), color=black)
result.add(diode.result, name="d2_1n5822",
           loc=at(base.diodes_x, base.d2_y, base.diodes_z, cq.Vector(1, -1, 0), 180), color=black)

# R6 and R2, soldered inline
inline_tan = cq.Color(0.80, 0.70, 0.50)
result.add(inline.result, name="r6_inline", loc=at(base.r6_x, base.r6_y, base.r6_z), color=inline_tan)
result.add(inline.result, name="r2_inline", loc=at(base.r2_x, base.r2_y, base.r2_z), color=inline_tan)

# D1: its anode lead (at its own x = -pitch / 2) in the VOUT+ hole
result.add(diode.result, name="d1_1n5822",
           loc=at(base.d1_x - diode.pitch / 2, base.d1_y, base.d1_z, cq.Vector(0, 1, -1), 180),
           color=black)

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
