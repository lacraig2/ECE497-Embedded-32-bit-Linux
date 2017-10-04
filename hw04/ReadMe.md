# Homework 4

## Requirements:
### Memory Map:
#### Description
Create a system memory map specifically for the Beagle. Do this by finding the Memory Map in the AM335x Technical Reference Manual (TRM).  It’s nine pages long, print it out (but not the whole 5,000+ page pdf file!) Using this as a reference, create a Beagle Bone version of Figure 2-5 (no more than a page long). Be sure to find:
1. a numeric value for the starting address of the EMIF0 SDRAM,
2. base addresses for each of the four 32-bit GPIO ports.

### GPIO via mmap
So far we’ve used the sysfs to access the GPIO registers through /sys/class/gpio.  All the GPIO is memory mapped so it can be accessed simply by accessing the correct memory location, much like GPIO is done on a PIC.  See EBC gpio via mmap on eLinux.org for examples of how mmap() allows you to access registers directly.
1. Write a C program that reads from at least two switches and controls two LEDs (the built-in LEDs are fine). The GPIO pins used for the switches need to be from two different GPIO ports. This means you will have to use two separate mmap() calls.
2. Modify gpioThru.c to read from a switch and control an LED.

### Rotary Encoders
Modify your Etch-a-Sketch to use two rotary encoders. exerciese/sensors/eQEP has an example of how to read an encoder in Python.


## Work
### Memory Map
#### Description
- For this I used the TRM and made the [bb_blue_mmap_from_trm.pdf](bb_blue_mmap_from_trm.pdf) file which contains the 9 pages from the TRM that are relevant to the mmap assignment. I used the values here to create [bb_blue_mmap.pdf](bb_blue_mmap.pdf) using values I thought seemed relevant and required values.

### GPIO via mmap
#### Description
- For this I modified gpioThru.c and gpioToggle.c from the examples and created [gpioViaMmap.c](gpioViaMmap.c).

### Rotary Encoders
- For this I really just added some simple logic to the encoders to update values based on the direction the rotary encoders moved. This was implemented in [i2cmatrix.py](i2cmatrix.py). I couldn't get it to work with the pushbuttons since the pushbuttons work only for me in Python 2 and the rcpy library supports only Python 3. ¯\\_(ツ)_/¯


### Requirements:
A unix system with Python 2 or 3. This only requires the curses library in python (should be default on Unix systems).

### Instructions:
Use buttons attached to GPIO pins to move the cursor. Use the PAUSE button to clear.

### Usage:

#### Memory Map
- None

#### GPIO via mmap
- Compile with the following snippet:
	`gcc -Wall -o3 gpioViaMmap.c -o gpioViaMmap`
- Run the program by executing:
	`sudo ./gpioViaMmap` (probably needs root priviledges)

#### Rotary Encoders

- This sets up an 8x8 etch a sketch game. (default)

    `python etch_a_sketch.py`

- This sets up a 9x9 etch a sketch game.

    `python etch_a_sketch.py -n 9`

- This sets up a 7x4 etch a sketch game.

    `python etch_a_sketch.py -n 7 -m 4`



