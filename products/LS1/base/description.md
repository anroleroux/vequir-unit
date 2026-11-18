A rectangular box like the PB6 base, but for only one battery: open at the
top, with the sides at +y and -y removed and the end walls at +x (front) and
-x (back) kept, so it is a floor and two end walls. Four variables drive its
size: l (length), b (breadth), h (height) and the wall thickness; the walls
and the floor are all one wall thickness thick.

A single 18650 holder with its cell (library
battery_holders/single_18650_holder) is glued on the floor against the back
wall, along the -y side, with the single-cell BMS strip (Mantech 210454) on
top of the cell.

Behind the LED strip on the lid, a Raspberry Pi Pico 2 W is mounted on its
side, fixed with M1.2 countersunk screws to pillars rising from the floor.
Behind the Pico, the MT3608 boost converter is also mounted on its side, held
by pillars.

In front of the holder, a perfboard (the wiring board) is raised into the
upper half of the box on pillars rising from the floor, screwed down with
M1.2 countersunk screws. It reaches forward to the front wall and carries the
buzzer and the bare DS18B20 at its front, then the three 1N5822 diodes, the
resistors (among them the battery voltage divider and the LED stick's data
resistor), a capacitor and the buzzer's transistor.

Under it, the TP4056 charger lies on the floor right behind the USB-C
board, held at its corners by four pillars. The horizontal USB-C breakout is
raised a little and moved forward into the front wall, in an inset that
leaves its connector 0.4 mm from the outside, with a hole for the plug; a
clamp across the connector, screwed down to two posts with M1.2 countersunk
screws, presses it down. The front wall has vent holes.

The TSD-1166 LED push button goes through a round hole in the back wall: its
body against the inside of the wall, its button sticking out.
