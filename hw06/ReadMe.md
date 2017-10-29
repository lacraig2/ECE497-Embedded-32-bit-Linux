# Homework 6

## Requirements:
### 2.4” TFT LCD Display
The goal of this homework is to play with the 2.4” LCD display.
Plug in and turn on
Attach the cable to the LCD display and to the Bone.
### Display Images
- Follow the instructions in install.sh to download fbi and some images.  Display them with:
	- `bone$ fbi -noverbose -T 1 -a boris.png`
- You should now see Boris the Beagle on your display.  Look in reset.sh (or install.sh) and figure out how to rotate the display.  Rotate Boris 90°.

### Play Movies
- Install mplayer and load a movie on the Bone (see install.sh).  Play the movie.  Rotate the movie.

### Generate Text
- Install imagemagick.  See text.sh for an example of using imagemagick to write text to the LCD display.  Write your name on the LCD.  Display an image and write some text on it.

### Pygame
- If you have used pygame before, try running it on the display.

### Writing pixels to the LCD
Look at the code in framebuffer.c and etch-a-sketch.c. Improve etch-a-sketch.  Ideas for improvement are:
- Draw a wider line.  
- Allow the user to select the line width.
- Allow use to select the line color.
- Have an erase mode.
- etc.



## Work
### 2.4” TFT LCD Display
- Here I simply plugged in and used the install script and then the on script to turn on the LCD display. This did not work initially, but upon restarting the device the on script worked properly.

### Display Images
- I got this to work with the provided command and then modified the reset script and created [display_images.sh](display_images.sh) which displays the dog rotated 90 degrees.s

### Play Movies
- I got this to work simply using mplayer. I was able to play several movies, but while I was able to get the movie to play rotated with a combination of:
	- `modprobe fbtft_device name=adafruit28 busnum=1 rotate=0 gpios=reset:113,dc=116 cs=0`
	- `mplayer (video file)`
- However, I could not get it to shrink down the movie. It still plays cut off. mplayer has options to scale this, but I don't think the bone has the hardware to be able to support this properly.

### Generate Text
- I started with [text.sh](text.sh) and created [luke_text.sh](luke_text.sh) with knowledge from [this link](https://www.imagemagick.org/Usage/draw/) to write text over the image. It was pretty neat.

### Pygame
- The instructions say 'if you have tried pygame'. I have never used pygame so I suppose I don't need to do this part? At least, that is my reading of this.

### Writing pixels to the LCD
- I modified the original (preserved in [etch-a-sketch-original.c](etch-a-sketch-original.c)) program of Dr. Yoder's to take an argument 



### Requirements:
- The install script should take care of most things. [install.sh](install.sh).

### Instructions:
- Use the rotary encoders to play the etch-a-sketch game.

### Usage:
#### matrixLED
- `sudo nodejs boneServer.js` (usually requires extended priviledges)

#### Etch-A-Sketch
- `make`
- `sudo ./etch-a-sketch [dot size] [line color]`
	- dot size: integer (e.g. 20) (default: 1)
	- line color: red, green, blue, black, or yellow. (default: green)