# Homework 2

## Requirements:
### Buttons and LEDs:
#### Description
1. Wire up your breadboard to have 4 buttons.  Each is to have one terminal attached to +3.3V and the other to a GPIO port.
2. Also wire up 4 LEDs with current limiting resistors. Tie the plus side of the LED to the GPIO port and run the minus to the resistor and to ground. 
3. Write a simple program that reads the switches and lights a corresponding LED. Use interrupts.
#### Work
- For this I wired up the buttons and LEDs and wrote buttons_and_leds.py for this requirement
### Etch-a-sketch
#### Description
- Next write modify your Etch-a-sketch[1] program to be controlled by the pushbuttons.  I suggest converting to Python since the I/O is easy. For now just print the grid in the terminal window.  Next week we’ll interface it to the LED grid.
#### Work
- I used the work I did on Buttons and LEDs as the basis of the controls for this part and modified my Etch-a-sketch from HW1 to use the push buttons. The code is stored in etch_a_sketch.py. Instructions and requirements are listed below.


## Etch-a-sketch

### Requirements:
A unix system with Python 2 or 3. This only requires the curses library in python (should be default on Unix systems).

### Instructions:
Use buttons attached to GPIO pins to move the cursor. Use the PAUSE button to clear.

### Usage:

- This sets up an 8x8 etch a sketch game. (default)

    `python etch_a_sketch.py`

- This sets up a 9x9 etch a sketch game.

    `python etch_a_sketch.py -n 9`

- This sets up a 7x4 etch a sketch game.

    `python etch_a_sketch.py -n 7 -m 4`
