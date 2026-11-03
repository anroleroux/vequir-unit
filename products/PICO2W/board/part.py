"""Raspberry Pi Pico 2 W.

The Pico 2 W microcontroller board: a 1 mm board with the RP2350, its flash,
the CYW43439 wireless module under a shield can, a micro-USB port, the
BOOTSEL button, 40 edge pins (through-holes and castellations), three SWD
debug pads and four mounting holes.

Assumptions where the description is silent:
- the pin through-holes are 1.0 mm and the castellations 1.0 mm half-holes
  centred on the board's long edges, in line with the through-holes;
- the micro-USB receptacle is 7.5 mm wide, 5.0 mm deep and 2.6 mm high, its
  mouth 1.3 mm proud of the board's end, centred across the board;
- the RP2350 (QFN-60) is a 7 x 7 x 0.9 mm block 17 mm from the USB end; the
  flash a 3 x 2 x 0.6 mm block beside the port; the BOOTSEL button a
  3.5 x 4.5 x 1.0 mm block beside the flash;
- the wireless module's shield can is 10 x 10 x 1.6 mm, centred 38 mm from
  the USB end; the antenna beyond it is a copper trace, not modelled;
- the SWD pads are three 1.0 mm through-holes at 2.54 mm pitch across the
  board, 29 mm from the USB end, between the RP2350 and the can;
- the parts' sizes and places are typical, not measured; the copper of the
  pads and castellations is not modelled;
- x runs along the board with the USB end at -x, y across it, z up; the
  board is centred on x and y and its underside is on z = 0.
"""
import cadquery as cq

# the board, in mm
length = 51.0  # along x
width = 21.0  # along y
pcb_t = 1.0  # board thickness

# the pins
pins_per_side = 20
pin_pitch = 2.54  # along x
pin_rows = 17.78  # the two rows, centre to centre along y
pin_hole = 1.0  # through-hole diameter
castellation = 1.0  # half-hole diameter, centred on the edge

# the mounting holes
mount_hole = 2.1  # diameter
mount_x = 47.0  # apart along the board
mount_y = 11.4  # apart across it

# the debug pads
swd_count = 3
swd_x = 29.0  # from the USB end
swd_hole = 1.0  # diameter

# the micro-USB receptacle, at -x
usb = (5.0, 7.5, 2.6)  # deep (x), wide (y), high (z)
usb_overhang = 1.3  # its mouth past the board's end

# the other parts: along x, along y, high; centres from the USB end and the board's centre line
rp2350 = (7.0, 7.0, 0.9)
rp2350_x = 17.0
flash = (3.0, 2.0, 0.6)
flash_at = (9.0, -5.0)
bootsel = (3.5, 4.5, 1.0)
bootsel_at = (9.0, 5.0)
can = (10.0, 10.0, 1.6)  # the wireless module's shield
can_x = 38.0

height = pcb_t + usb[2]  # overall: the USB receptacle is the tallest part
x0 = -length / 2  # the USB end

pin_x = [x0 + length / 2 + (i - (pins_per_side - 1) / 2) * pin_pitch for i in range(pins_per_side)]
board = (
    cq.Workplane("XY").box(length, width, pcb_t, centered=(True, True, False))
    .faces(">Z").workplane()
    .pushPoints([(x, s * pin_rows / 2) for x in pin_x for s in (-1, 1)])
    .hole(pin_hole)
    .faces(">Z").workplane()
    .pushPoints([(x, s * width / 2) for x in pin_x for s in (-1, 1)])
    .hole(castellation)
    .faces(">Z").workplane()
    .pushPoints([(sx * mount_x / 2, sy * mount_y / 2) for sx in (-1, 1) for sy in (-1, 1)])
    .hole(mount_hole)
    .faces(">Z").workplane()
    .pushPoints([(x0 + swd_x, (i - (swd_count - 1) / 2) * pin_pitch) for i in range(swd_count)])
    .hole(swd_hole)
)


def block(size, x, y=0.0):
    """A part on top of the board, its centre x from the USB end."""
    return (cq.Workplane("XY", origin=(x0 + x, y, pcb_t))
            .box(*size, centered=(True, True, False)))


usb_x = -usb_overhang + usb[0] / 2  # from the USB end
parts = [
    block(usb, usb_x),
    block(rp2350, rp2350_x),
    block(flash, *flash_at),
    block(bootsel, *bootsel_at),
    block(can, can_x),
]
result = board
for p in parts:
    result = result.union(p)

regions = {
    "usb_end": result.faces("<X"),  # the micro-USB receptacle's mouth
    "mounting_holes": result.faces("%CYLINDER").filter(  # the four 2.1 mm holes' walls
        lambda f: abs(f.BoundingBox().xlen - mount_hole) < 1e-3 and abs(f.BoundingBox().ylen - mount_hole) < 1e-3),
    "bottom": result.faces("<Z"),
}

if "show_object" in globals():  # CQ-editor
    show_object(result, name="part")
