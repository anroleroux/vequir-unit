A rectangular box like the PB6 base, but for only one battery: open at the
top, with the sides at +y and -y removed and the end walls at +x (front) and
-x (back) kept, so it is a floor and two end walls. Four variables drive its
size: l (length), b (breadth), h (height) and the wall thickness; the walls
and the floor are all one wall thickness thick.

An off-the-shelf single-cell 18650 holder with wire leads (Micro Robotics
18650-1S-WIRE) and its cell are glued on the floor against the back wall,
along the -y side, with the single-cell BMS strip (Mantech 210454) on top
of the cell.

Behind the LED strip on the lid, a Raspberry Pi Pico 2 W is mounted on its
side, 4 mm away from the switch, fixed with M1.2 x 6 countersunk screws to
pillars rising from the floor at both ends. Four resistors are soldered
directly on its pins 2 to 5 (three GPIO pins and a GND pin), pointing -y.
Behind the Pico, the MT3608 boost converter is also mounted on its side,
held by pillars, 4 mm away from the TP4056 and moved toward the battery.

At the front, the horizontal USB-C breakout is raised a little and moved
forward into the front wall, in an inset that leaves its connector 0.4 mm
from the outside, with a hole for the plug; a clamp across the connector,
screwed down to two posts with M1.2 countersunk screws, presses it down.
The front wall has vent holes.

Right after the USB-C breakout, a small perfboard (the wiring board), cut as
short as its parts allow, stands up facing the front (+x), the buzzer at the
top and its longest side across the box. It carries the buzzer, the bare
DS18B20, the buzzer's transistor, the battery voltage divider (two
resistors and a capacitor) and the remaining resistors, all moved as far
as they go to its +y side, and a 10-pin box header at its -y side that
points -y and touches the inside of the lid, where the lid has a hole for
the cable.

Behind the perfboard, the TP4056 charger stands across the box facing
backwards (-x), in almost the same place. The bottoms of both boards lie in
slots in the floor. A clamp at the top, screwed with an M1.2 x 6
countersunk screw to a pillar that comes up between the two boards, has a
slot on either side that presses down on the top of each board and holds
it. Behind the TP4056, the three 1N5822 diodes lie across the box one
above the other in a pillar with three holes: D1 at the top, above the two
load-sharing diodes (D2 and D3). Their leads are straight and short, to be
wired there, and they sit toward -y, 4 mm away from the lid.

The TSD-1166 LED push button goes through a round hole in the back wall: its
body against the inside of the wall, its button sticking out.

The LED stick's data resistor is soldered inline at its input. The button
LED's resistor stands between the button's legs, in line with the button
along z, not connected (hovering in the air).

The LED stick on the lid is centred along the box's side.

On the lid, a 5 mm IR LED sits at each end of the LED stick and a 5 mm
phototransistor (Micro Robotics BP0334) above the middle of the stick,
each through a hole in the lid's side.
