"""PB6, assembled.

The PB6 powerbank: the base with the six-cell 18650 pack from the parts
library (vequir-power's battery_holders/pack_3x2) on its floor, three holders
side by side across the breadth, in two rows, their length along x, its back
end against the base's back end wall (-x). Two IP6505 USB fast-charge boards
sit side by side on the floor in front of the pack, their USB ports against
the front wall, each behind one of the wall's USB-A holes, and a CN3302 2S
charger board sits beside them at +y, its USB-C port behind the wall's USB-C
hole; the boards are bought in, from vequir-standard's power category. Eight
M1.2 x 6 countersunk screws, two through each of the end strips' four tabs,
fix the pack to the base's pillars. The lid is seated on top: its plate
rests on the base's end walls, its skirts close the open long sides down to
the base's bottom, and its lips drop just inside the end walls.

The base and the lid come from their own scripts through load_part, the pack,
boards and screws through load_library, so the model follows any change to
them.

The summary's interference lists each screw against what it is screwed into
(the base's pillars, and inside the pack the holders and the strips): each
one a screw's 1.2 mm shank forming its thread in a 0.95 mm tap hole, as
intended, and marked as a thread.

Assumptions where the description is silent:
- the pack is centred across the breadth and stands on the floor, its back
  end (the tips of its back end strip's tabs) against the back wall;
- the cells are wired as two groups of three in parallel, in series (2S3P,
  8.4 V full), to suit the 2S charger; the wiring is not modelled.
"""
import cadquery as cq

base = load_part("base")  # floor and end walls at +-x, standing on z = 0
lid = load_part("lid")  # modelled as installed: skirts stand on z = 0
pack = load_library("battery_holders/pack_3x2")  # the six-cell pack, standing on z = 0
ip6505 = load_library("power/ip6505_charger")  # USB-A port at +x, underside on z = 0
cn3302 = load_library("power/cn3302_charger")  # USB-C port at +x, underside on z = 0
screw = load_library("hardware/m1_2x6_countersunk")  # standing up: tip on z = 0

pack_loc = cq.Location((base.pack_dx, base.pack_dy, base.pack_dz))
lid_seat = base.h - lid.seat_height

result = (
    cq.Assembly(name="PB6")
    .add(base.result, name="base", color=cq.Color(0.36, 0.56, 0.78))
    .add(pack.result, name="pack_3x2", loc=pack_loc)
)

board_green = cq.Color(0.15, 0.45, 0.30)
for i, y in enumerate(base.ip6505_ys):
    result.add(
        ip6505.result,
        name=f"ip6505_charger_{i + 1}",
        loc=cq.Location((base.ip6505_x, y, base.ip6505_z)),
        color=board_green,
    )
result.add(
    cn3302.result,
    name="cn3302_charger",
    loc=cq.Location((base.cn3302_x, base.cn3302_y, base.cn3302_z)),
    color=board_green,
)

screw_top = base.pack_dz + pack.tab_top
for i, (x, y) in enumerate(base.pillar_holes, start=1):
    result.add(screw.result, name=f"pillar_screw_{i}",
               loc=cq.Location((x, y, screw_top - screw.length)),
               color=cq.Color(0.70, 0.70, 0.72))

result.add(lid.result, name="lid", loc=cq.Location((0, 0, lid_seat)),
           color=cq.Color(0.40, 0.68, 0.45))

regions = {}

if "show_object" in globals():  # CQ-editor (load_part runs under the CAD tool only)
    show_object(result, name="PB6")
