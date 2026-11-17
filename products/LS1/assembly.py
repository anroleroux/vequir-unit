"""LS1, assembled.

The LS1: the base with a single 18650 holder and its cell (vequir-power's
battery_holders/single_18650_holder) on the floor against the back wall
along the -y side; an MT3608 boost board and the single-cell BMS strip on
the floor beside it at +y; a horizontal USB-C breakout in front of the
holder, its receptacle behind the front wall's plug hole; and the TSD-1166
LED push button through the back wall, its body against the wall's inside.
The lid is seated on top, and the WS2812 8 x 1 stick sits against the
inside of its +y skirt, each LED in its window. The bought-in parts come
from vequir-standard.

The base and the lid come from their own scripts through load_part, the
rest through load_library, so the model follows any change to them.

Assumptions where the description is silent:
- the button is turned so its button points out through the back wall
  (-x), its legs into the box;
- the stick is turned a quarter turn about x so its LEDs face +y and its
  -y edge (the LEDs' side) is at the top;
- nothing is wired or fixed: wires, solder, glue and screws are not modelled.
"""
import cadquery as cq

base = load_part("base")  # floor and end walls at +-x, standing on z = 0
lid = load_part("lid")  # modelled as installed: skirts stand on z = 0
holder = load_library("battery_holders/single_18650_holder")
boost = load_library("power/mt3608_boost")
bms = load_library("power/bms_1s_3a")
usbc = load_library("electronics/usb_c_breakout")
button = load_library("electronics/tsd_1166_button")
stick = load_library("electronics/ws2812_stick_8")

board_green = cq.Color(0.15, 0.45, 0.30)
board_blue = cq.Color(0.15, 0.30, 0.60)

# the button: a quarter turn about y takes its +z (the button) to -x; its
# body's top (button.body_top up its axis) against the back wall's inside
button_x = -base.l / 2 + base.wall + button.body_top
# the stick: a quarter turn about x takes its +z (the LEDs) to +y
stick_loc = cq.Location(cq.Vector(lid.stick_x, lid.stick_y, lid.stick_z), cq.Vector(1, 0, 0), -90)

result = (
    cq.Assembly(name="LS1")
    .add(base.result, name="base", color=cq.Color(0.36, 0.56, 0.78))
    .add(holder.result, name="single_18650_holder",
         loc=cq.Location((base.holder_dx, base.holder_dy, base.holder_dz)))
    .add(boost.result, name="mt3608_boost",
         loc=cq.Location((base.boost_x, base.boost_y, base.boost_z)), color=board_blue)
    .add(bms.result, name="bms_1s_3a",
         loc=cq.Location((base.bms_x, base.bms_y, base.bms_z)), color=board_green)
    .add(usbc.result, name="usb_c_breakout",
         loc=cq.Location((base.usbc_x, base.usbc_y, base.usbc_z)), color=board_blue)
    .add(button.result, name="tsd_1166_button",
         loc=cq.Location(cq.Vector(button_x, base.button_y, base.button_z), cq.Vector(0, 1, 0), -90),
         color=cq.Color(0.12, 0.12, 0.12))
    .add(stick.result, name="ws2812_stick_8", loc=stick_loc, color=cq.Color(0.10, 0.10, 0.10))
    .add(lid.result, name="lid", loc=cq.Location((0, 0, base.h - lid.seat_height)),
         color=cq.Color(0.40, 0.68, 0.45))
)

regions = {}

if "show_object" in globals():  # CQ-editor (load_part runs under the CAD tool only)
    show_object(result, name="LS1")
