# Homework 3

## Requirements:
### TMP101:
#### Description
1. Wire up your two TMP101 on the i2c bus so each has a different address. Also wire the ALERT pin to a GPIO port.
2. Use the shell commands to read the temperature of each. Write a shell file to read the temperature and convert it to Fahrenheit.  Hint:  temp=`i2cget -y 1 0x48` assigns the output of i2cget to the variable temp.  Hint 2: temp2=$(($temp *2)) multiplies temp by two.
3. Use the i2cset command to set the temperature limits THIGH and TLOW. Test that they are working.
4. Write a program that sets the temperature limits on each TMP101 and waits for an interrupt on the ALERT pin, then prints the temperature in F.  To keep things simple you may use a shell file to set things up.


### Etch-a-sketch
Modify your etch-a-sketch program to use the bicolor LED matrix in your kit.  The matrix will work off of 3.3V.
1. Wire the matrix up to the same bus as your TMP101’s.
2. Use the programs in exercises/displays/matrix8x8 to set the matrix before modifying your Etch-a-sketch program.
3. Once working, interface the LED matrix to your Etch-a-sketch.


## Work
### TMP101
#### Description
- For this I attempted to get it to read properly. THIS DOES NOT FULLY WORK. It reads, but it does not alert more than once.

### Etch-A-sketch
#### Description
- I used an abstraction layer for the Matrix system and then added the logic to the Game class. This implemented the game properly.

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
