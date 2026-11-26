"""LS1 USB-C clamp.

A flat bar across the USB-C breakout's receptacle, screwed at both ends to
the base's two clamp posts with M1.2 x 6 countersunk screws, its underside
pressing on the receptacle's top. A tongue the receptacle's width runs
back from it over the receptacle, past the metal shell's back, with a lip
that comes down behind the shell, so the receptacle is held against a plug
being pushed in. Sized from the base, so it follows the posts and the
receptacle.

Assumptions where the description is silent:
- the bar is 4 mm wide (along x) and 2.5 mm thick, and reaches to the far
  sides of the two 3.5 mm posts;
- the tongue is the shell's width plus 1 mm each side and as thick as the
  bar; the lip is 1.2 mm thick, 0.2 mm behind the shell's back, and comes
  down to 0.3 mm above the breakout's board (the box's clamp_* values);
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
# the tongue back over the receptacle, past its back, and the lip down behind
# it, so the receptacle is held against a plug pushed in (box values are in
# the box's coordinates; this part's x = 0 is the box's clamp_x, its z = 0
# the box's clamp_z)
lip_x0 = box.clamp_lip_x0 - box.clamp_x
lip_x1 = box.clamp_lip_x1 - box.clamp_x
tongue_w = box.clamp_tongue_w
lip_drop = box.clamp_z - box.clamp_lip_bottom  # below the underside
tongue = (cq.Workplane("XY", origin=(lip_x0, -tongue_w / 2, 0))
          .box(-width / 2 - lip_x0, tongue_w, thickness, centered=False))
lip = (cq.Workplane("XY", origin=(lip_x0, -tongue_w / 2, -lip_drop))
       .box(lip_x1 - lip_x0, tongue_w, lip_drop, centered=False))
bar = bar.union(tongue).union(lip)
for y in hole_ys:
    hole = cq.Workplane("XY", origin=(0, y, 0)).circle(clearance_hole / 2).extrude(thickness)
    bore = cq.Workplane("XY", origin=(0, y, thickness - edge_h)).circle(sink_r).extrude(edge_h)
    cone = cq.Solid.makeCone(clearance_hole / 2, sink_r, cone_h,
                             cq.Vector(0, y, thickness - edge_h - cone_h))
    bar = bar.cut(hole).cut(bore).cut(cq.Workplane("XY").add(cone))
result = bar

regions = {
    "underside": result.faces("%PLANE").filter(  # on the receptacle and the posts
        lambda f: f.normalAt().z < -0.999 and abs(f.Center().z) < 1e-6),
    "lip_face": result.faces("%PLANE").filter(  # behind the receptacle's back
        lambda f: f.normalAt().x > 0.999 and abs(f.Center().x - lip_x1) < 1e-6),
    "top": result.faces(">Z"),
    "screw_holes": result.faces("%CYLINDER").filter(
        lambda f: abs(f.BoundingBox().xlen - clearance_hole) < 1e-3),
}

if "show_object" in globals():  # CQ-editor (load_part runs under the CAD tool only)
    show_object(result, name="part")
