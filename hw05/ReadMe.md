# Homework 5

## Requirements:
### matrixLED
Dr. Yoder's  matrixLED.js only controls one of the two LEDs in the matrix.  Your task is to make it control both LEDS. One approach would be to have the first click turn on the Green LED, the 2nd turn on both, the 3rd would turn on only the Red LED and the 4th click turns both off.
1. Before writing any code, write a paragraph describing how boneServer.js and the browser interact in the given example. For example, in matrixLED.js connect() is called to make a connection between the browser and the bone.  The message “matrix” is sent to the bone. What happens in response to the message? 
2. What happens when an “LED” is clicked on in the browser?
3. What entry in matrix.css is used to color the LED?
4. Write a high level paragraph about how you will control the two LEDs. What messages will be sent between the browser and the bone?
5. Write your code.  Do you need to change boneServer.js? (I don’t think so.)  Customize the html to have your name on it, etc.


## Work
### matrixLED
1. 


### Requerements:
A unix system with Python 2 or 3. This only requires the curses library in python (should be default on Unix systems).

### Instructions:
Use buttons attached to GPIO pins to move the cursor. Use the PAUSE button to clear.

### Usage:
#### matrixLED
- `sudo nodejs boneServer.js` (usually requires extended priviledges)
