"""LS1 USB-C clamp.

A flat bar across the USB-C breakout's receptacle, screwed at both ends to
the base's two clamp posts with M1.2 x 6 countersunk screws, its underside
pressing on the receptacle's top. Sized from the base, so it follows the
posts.

Assumptions where the description is silent:
- the bar is 4 mm wide (along x) and 2.5 mm thick, and reaches to the far
  sides of the two 3.5 mm posts;
- each screw hole is an M1.2 clearance (1.3 mm) with a 90 degree countersink
  for the 2.3 mm head (0.05 mm clearance round it), so the head sits flush;
- modelled standing on z = 0 (its underside), centred.
"""
import cadquery as cq

box = load_part("../base")  # the clamp posts: their places and size
screw = load_library("hardware/m1_2x6_countersunk")

# in mm
width = box.clamp_w  # along x
thickness = box.clamp_t
clearance_hole = 1.3  # M1.2
head_clearance = 0.05  # radial, round the head

length = 2 * (box.clamp_post_y + box.clamp_post / 2)  # along y, over both posts
hole_ys = [-box.clamp_post_y, box.clamp_post_y]
sink_r = screw.head_diameter / 2 + head_clearance
cone_h = sink_r - clearance_hole / 2  # 90 degrees: as deep as it narrows
edge_h = screw.edge_height

bar = cq.Workplane("XY").box(width, length, thickness, centered=(True, True, False))
for y in hole_ys:
    hole = cq.Workplane("XY", origin=(0, y, 0)).circle(clearance_hole / 2).extrude(thickness)
    bore = cq.Workplane("XY", origin=(0, y, thickness - edge_h)).circle(sink_r).extrude(edge_h)
    cone = cq.Solid.makeCone(clearance_hole / 2, sink_r, cone_h,
                             cq.Vector(0, y, thickness - edge_h - cone_h))
    bar = bar.cut(hole).cut(bore).cut(cq.Workplane("XY").add(cone))
result = bar

regions = {
    "underside": result.faces("<Z"),  # on the receptacle and the posts
    "top": result.faces(">Z"),
    "screw_holes": result.faces("%CYLINDER").filter(
        lambda f: abs(f.BoundingBox().xlen - clearance_hole) < 1e-3),
}

if "show_object" in globals():  # CQ-editor (load_part runs under the CAD tool only)
    show_object(result, name="part")
