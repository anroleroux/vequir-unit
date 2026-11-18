A rectangular box like the PB6 base, but for only one battery: open at the
top, with the sides at +y and -y removed and the end walls at +x (front) and
-x (back) kept, so it is a floor and two end walls. Four variables drive its
size: l (length), b (breadth), h (height) and the wall thickness; the walls
and the floor are all one wall thickness thick.

A single 18650 holder with its cell (library
battery_holders/single_18650_holder) is glued on the floor against the back
wall, along the -y side. A TP4056 USB-C charger module with protection lies
on the holder's front end, and the single-cell BMS strip (Mantech 210454)
lies on the holder behind it, on top of the cell.

Behind the LED strip on the lid, a Raspberry Pi Pico 2 W is mounted on its
side, fixed with M1.2 countersunk screws to pillars rising from the floor.
Behind the Pico, the MT3608 boost converter is also mounted on its side, held
by pillars.

In front of the holder, a small perfboard (the wiring board) holds the
three 1N5822 diodes, the three resistors and the buzzer's transistor; it is
screwed with M1.2 countersunk screws to pillars rising from the floor. The
box is made longer to fit it.

In front of the holder a horizontal USB-C breakout board sits on pillars with
its receptacle against the inside of the front wall, and the front wall has a
hole for a USB-C plug in line with it.

The TSD-1166 LED push button goes through a round hole in the back wall: its
body against the inside of the wall, its button sticking out. The 5 V active
buzzer stands on the floor beside it, and a bare DS18B20 measures the air
inside the box.
