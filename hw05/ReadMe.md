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
1. I wrote this high level paragraph as a response to Q1:
	- The systems work by a system of callbacks on events. These events are sent throught the client-side javascript to the server side javascript. Some of these events are startup, click, and shutdown. The matrix function returns a string of the return from the i2cdump.
2. I wrote this response as an answer to Q2:
	- A socket.emit is called, which the server listens for, and the server calls a subprocess with the appopriate arguments to i2cset (a system call).
3. I wrote this response as an answer to Q3:
	- The "on" class is used as the green color.
4. I wrote this high-level paragraph as a response to Q4:
	- I am going to adjust the I am going to use the CSS classes and the use those classes to track javascript structures to save the state of the array. Then I am going to adjust the method to check the initial state to represent these structures. Then I am going to change ledClick() to use these structures. Then I am going to write a method to return the hex values to pass to i2cset.

5. I started from Dr. Yoder's realtime folder.
6. I added CSS classes to be able to have green, red, and yellow states. I adjusted this in [matrixLED.css](matrixLED.css). 
7. I changed [matrixLED.js](matrixLED.js) to to use the CSS classes.
8. I changed [matrixLED.js](matrixLED.js) to use the added classes to track javascript structures. 
9. I changed [matrixLED.js](matrixLED.js) to use the method to check the initial state to represent these structures. 
10. I changed [matrixLED.js](matrixLED.js) to change ledClick() to use these structures. 
11. I changed [matrixLED.js](matrixLED.js) to write a method to return the hex values to pass to i2cset.
12. At this point it worked properly (though I had a lot of trouble with implementation. As it turns out my representation needed to be reversed in the x and y direction).


### Requirements:
nodejs.

### Instructions:
Use buttons attached to GPIO pins to move the cursor. Use the PAUSE button to clear.

### Usage:
#### matrixLED
- `sudo nodejs boneServer.js` (usually requires extended priviledges)
