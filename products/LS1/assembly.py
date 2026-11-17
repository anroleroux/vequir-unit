"""LS1, assembled.

The LS1: the base with a single 18650 holder and its cell (vequir-power's
battery_holders/single_18650_holder) glued on the floor against the back
wall along the -y side, the single-cell BMS strip lying on the cell. Along
the +y side a Pico 2 W stands on its side, screwed to the base's four posts
with M1.2 x 3 countersunk screws, and behind it the MT3608 boost board
stands on its side in two slotted posts. A horizontal USB-C breakout sits on
two pegged pillars at the front, its receptacle behind the front wall's plug
hole; the TSD-1166 LED push button goes through the back wall; the active
buzzer stands beside it, and the bare DS18B20 in the air at the front. The
lid is seated on top, and the WS2812 8 x 1 stick is screwed to two pillars
inside its +y skirt with M1.2 x 3 countersunk screws, each LED in its
window, in front of the Pico. The bought-in parts come from vequir-standard.

The base and the lid come from their own scripts through load_part, the
rest through load_library, so the model follows any change to them.

The summary's interference lists each screw against what it is screwed into
(the base's posts and the lid's pillars): a screw's 1.2 mm shank forming its
thread in a 0.95 mm tap hole, as intended, and marked as a thread.

Assumptions where the description is silent:
- the button is turned so its button points out through the back wall
  (-x), its legs into the box;
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
usbc = load_library("electronics/usb_c_breakout")
button = load_library("electronics/tsd_1166_button")
stick = load_library("electronics/ws2812_stick_8")
pico = load_library("electronics/pico_2w")
buzzer = load_library("electronics/buzzer_12x9")
sensor = load_library("electronics/ds18b20")
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
    .add(buzzer.result, name="buzzer", loc=at(base.buzzer_x, base.buzzer_y, base.buzzer_z), color=black)
    .add(sensor.result, name="ds18b20", loc=at(base.sensor_x, base.sensor_y, base.sensor_z), color=black)
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

result.add(lid.result, name="lid", loc=at(0, 0, base.h - lid.seat_height),
           color=cq.Color(0.40, 0.68, 0.45))

regions = {}

if "show_object" in globals():  # CQ-editor (load_part runs under the CAD tool only)
    show_object(result, name="LS1")
