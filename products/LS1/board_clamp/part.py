"""LS1 board clamp.

A bar along x over the pillar between the wiring board and the TP4056,
screwed down to the pillar with one M1.2 x 6 countersunk screw, with an arm
at each end that comes down over a board's top edge: each arm has a slot
that the edge sits in, pressing the board down into its slot in the floor.
The TP4056's top edge is lower than the wiring board's, so its arm reaches
further down.

Assumptions where the description is silent:
- the clamp is the base's bc_w = 4 mm wide (along y), centred on the
  pillar; its bar is bc_t = 2 mm thick, its underside on the pillar's top,
  0.5 mm under the wiring board's top edge;
- each slot is the board's thickness plus 0.1 mm each side, taking 1.0 mm
  of the board's top edge, which presses on the slot's bottom; the walls
  either side are 1.2 mm, like the floor slots' (the base's rail_* values);
- the screw goes through an M1.2 clearance hole (1.3 mm), countersunk so
  its head is flush with the bar's top;
- modelled as installed, in the box's coordinates (the base's x, y and z),
  so the assembly places it as it is.
"""
import cadquery as cq

box = load_part("../base")  # the boards' places, the pillar and the clamp's sizes
screw = load_library("hardware/m1_2x6_countersunk")

# in mm
width = box.bc_w  # along y
clearance_hole = 1.3  # M1.2
head_clearance = 0.05  # radial, round the head
wall = box.rail_wall  # either side of each slot
engage = box.rail_engage  # of each board's top edge in its slot

y0 = box.pillar_y - width / 2
bottom, top = box.bc_bottom, box.bc_top
tp_x0, tp_x1 = box.tp_slot_x  # the TP4056's slot, across x
wb_x0, wb_x1 = box.wb_slot_x  # the wiring board's
tp_edge = box.charger_top  # its top edge
wb_edge = box.wb_top
x0, x1 = tp_x0 - wall, wb_x1 + wall  # the bar's ends
assert tp_edge - engage < bottom and wb_edge - engage < bottom, "an arm does not reach its board"


def block(xa, xb, za, zb):
    return cq.Workplane("XY", origin=(xa, y0, za)).box(xb - xa, width, zb - za, centered=False)


bar = block(x0, x1, bottom, top)
tp_arm = block(x0, tp_x1 + wall, tp_edge - engage, bottom)
wb_arm = block(wb_x0 - wall, x1, wb_edge - engage, bottom)
slots = block(tp_x0, tp_x1, tp_edge - engage, tp_edge).union(block(wb_x0, wb_x1, wb_edge - engage, wb_edge))

sink_r = screw.head_diameter / 2 + head_clearance
cone_h = sink_r - clearance_hole / 2  # 90 degrees: as deep as it narrows
edge_h = screw.edge_height
px, py = box.pillar_x, box.pillar_y
hole = cq.Workplane("XY", origin=(px, py, bottom)).circle(clearance_hole / 2).extrude(top - bottom)
bore = cq.Workplane("XY", origin=(px, py, top - edge_h)).circle(sink_r).extrude(edge_h)
cone = cq.Solid.makeCone(clearance_hole / 2, sink_r, cone_h, cq.Vector(px, py, top - edge_h - cone_h))

result = (bar.union(tp_arm).union(wb_arm).cut(slots)
          .cut(hole).cut(bore).cut(cq.Workplane("XY").add(cone)))

regions = {
    "top": result.faces(">Z"),
    "on_pillar": result.faces("%PLANE").filter(  # the bar's underside over the pillar
        lambda f: f.normalAt().z < -0.999 and abs(f.Center().z - bottom) < 1e-6
        and abs(f.Center().x - px) < box.pillar),
    "slot_bottoms": result.faces("%PLANE").filter(  # where the boards' top edges press
        lambda f: f.normalAt().z < -0.999 and (abs(f.Center().z - tp_edge) < 1e-6
                                              or abs(f.Center().z - wb_edge) < 1e-6)),
    "screw_hole": result.faces("%CYLINDER").filter(
        lambda f: abs(f.BoundingBox().xlen - clearance_hole) < 1e-3),
}

if "show_object" in globals():  # CQ-editor (load_part runs under the CAD tool only)
    show_object(result, name="part")
