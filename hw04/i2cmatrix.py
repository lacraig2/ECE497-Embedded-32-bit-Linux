#!/usr/bin/python

# By: Luke Craig
# Dr. Yoder
# ECE497 Embedded 32-bit Linux
# HW03

import smbus
from time import sleep
from random import randint
from curses import KEY_DOWN, KEY_UP, KEY_LEFT, KEY_RIGHT, curs_set, wrapper
from optparse import OptionParser
from math import log10
import Adafruit_BBIO.GPIO as GPIO
from time import sleep
from sys import exit
import rcpy 
import rcpy.encoder as encoder

GPIOs = {"GP0_3": GPIO.RISING, "GP0_4": GPIO.FALLING, "GP0_5": GPIO.RISING,"GP0_6": GPIO.FALLING}
game = None
stdscr = None

class Matrix:
	'''RGB TUPLES'''
	BLACK = (0,0)
	RED = (1,0)
	GREEN = (0,1)
	YELLOW = (1,1)

	def __init__(self, n, address, bus):
		self.matrix_red = [[0 for i in range(n)] for j in range(n)]
		self.matrix_green = [[0 for i in range(n)] for j in range(n)]
		self.address = address
		self.bus = bus
		self.bus.write_byte_data(address, 0x21, 0)   # Start oscillator (p10)
		self.bus.write_byte_data(address, 0x81, 0)   # Disp on, blink off (p11)
		self.bus.write_byte_data(address, 0xe7, 0)   # Full brightness (page 15)

	def set_pixel(self, x, y, color):
		self.matrix_red[x][y] = color[0]
		self.matrix_green[x][y] = color[1]
		self.update()

	def set_row(self, x, color):
		for i in range(len(self.matrix_red[0])):
			self.set_pixel(x,i, color)

	def set_col(self, x,color):
		for i in range(len(self.matrix_red)):
			self.set_pixel(i,x,color)

	def color(self, color_val):
		for i in range(len(self.matrix_red)):
			for j in range(len(self.matrix_red)):
				self.set_pixel(i,j, color_val)

	def clear(self):
		self.color(self.BLACK)

	def get_array(self):
		a = []
		for i in range(len(self.matrix_red)):
			a.append(get_num_from_arr(self.matrix_green[i]))
			a.append(get_num_from_arr(self.matrix_red[i]))
		return a

	def update(self):
		self.bus.write_i2c_block_data(self.address, 0, self.get_array())

def get_num_from_arr(arr):
	total = 0
	for i in range(len(arr)):
		if arr[::-1][i]==1:
			total += (1 << i)
	return total


class Game:
	def __init__(self, n, address, bus, m=None):
		'''The initializer for the game sets up the initial position and the game board'''
		if m is None:
			m = n
		self.n = n
		self.m = m
		self.x = 0
		self.y = 0
		#self.numspaces = num_spaces(self.n)
		#self.board = [[" " for j in range(n)] for i in range(m)]
		#self.live = True

		self.matrix = Matrix(n, address, bus)
		self.past_color = self.matrix.GREEN
		self.cursor_color = self.matrix.RED

		self.matrix.clear()
		self.matrix.set_pixel(self.x,self.y,self.cursor_color)
		

	#def __str__(self):
		'''This method returns the base string representation of the Game class.'''
	#	return "  "+" ".join([str(i).rjust(self.numspaces+1) for i in range(self.n)])+"\n"+ "\n".join([(str(i)+": ").rjust(2+self.numspaces)+(" ".rjust(self.numspaces+1)).join([self.board[i][j] for j in range(self.n)]) for i in range(self.m)])

	def up(self):
		'''Moves the position up and marks it. Thoughtful of bounds.'''
		x0 = self.x
		y0 = self.y
		self.x = self.x -1  if self.x > 0 else 0
		#self.board[self.x][self.y] = 'X'
		self.move_pos(self.x,self.y,x0,y0)

	def down(self):
		'''Moves the position down and marks it. Thoughtful of bounds'''
		x0 = self.x
		y0 = self.y
		self.x = self.x +1 if self.x < self.m-1 else self.m-1
		#self.board[self.x][self.y] = 'X'
		self.move_pos(self.x,self.y,x0,y0)
	
	def left(self):
		'''Moves the position left and marks it. Thoughtful of bounds'''
		x0 = self.x
		y0 = self.y
		self.y = self.y -1 if self.y > 0 else 0
		#self.board[self.x][self.y] = 'X'
		self.move_pos(self.x,self.y,x0,y0)
	
	def right(self):
		'''Moves the position right and marks it. Thoughtful of bounds'''
		x0 = self.x
		y0 = self.y
		self.y = self.y+1 if self.y < self.n -1 else self.n -1
		#self.board[self.x][self.y] = 'X'
		self.move_pos(self.x,self.y,x0,y0)
	
	def move_pos(self,x,y,x0,y0):
		if x==x0 and y == y0:
			return
		self.matrix.set_pixel(x0,y0, self.past_color)
		self.matrix.set_pixel(x,y, self.cursor_color)

	
	def clear(self):
		'''Clears the board to default values'''
		#self.board = [[" " for j in range(self.n)]for i in range(self.m)]
		self.matrix.clear()
		self.matrix.set_pixel(self.x,self.y, self.cursor_color)

#def num_spaces(n):
#	return int(log10(n))+1

'''
On globals:

Yes, these are globals. I use two. Game and screen.
I use game because I that has to be global in this context to be able to use a callback.
I use stdscr as a global because instead of using a while loop to update every 100 ms this
only calls update_screen when it needs to (on events). I think this is a better approach on th whole.
'''

#def update_game(channel):
#	if channel == "GP0_3":
#		game.up()
#	elif channel == "GP0_4":
#		game.left()
#	elif channel == "GP0_5":
#		game.down()
#	elif channel == "GP0_6":
#		game.right()
#	elif channel == "PAUSE":
#		game.clear()
#	update_screen()

'''
Simple method to update the curses screen.
'''
# def update_screen():
	# stdscr.addstr(0, 0, "Etch-a-sketch for ECE497-01 Embedded 32-bit Linux By: Luke Craig")
	# stdscr.addstr(1, 0, "USE YOUR GPIO Pins to move and PAUSE to clear.")
	# stdscr.addstr(2, 0, str(game))
	# stdscr.refresh()
	# curs_set(0) # this just prevents a blinking cursor

def main():
	# parse command line options
	parser = OptionParser()
	parser.add_option("-n", dest="n", help="n size argument to game")
	parser.add_option("-m", dest="m", help="m size argument to game")
	options,args = parser.parse_args()

	rcpy.set_state(rcpy.RUNNING)
	bus = smbus.SMBus(1)  # Use i2c bus 1
	matrixAddr = 0x70         # Use address 0x70

	global game
	# set up game with command line options
	if options.m and options.n:
		n = int(options.n)
		m = int(options.m)
		game = Game(n if n < 25 else 8, m if m < 25 else 8, address=matrixAddr, bus= bus)
	elif options.n:
		n = int(options.n)
		game = Game(n if n < 25 else 8, address=matrixAddr, bus= bus)
	else:
		game = Game(8,m = 8, address = matrixAddr, bus = bus) # default

	# set up PAUSE pin for clear functionality
	#GPIO.setup("PAUSE", GPIO.IN)
	#GPIO.add_event_detect("PAUSE", GPIO.BOTH, callback=update_game)

	# set up input pins
	#for i in GPIOs:
	#	GPIO.setup(i, GPIO.IN)
	#	GPIO.add_event_detect(i, GPIOs[i],callback=update_game)

	# update_screen()  

	# sleep  
	e2 = 0
	e3 = 0
	try:
		while True:
			if rcpy.get_state() == rcpy.RUNNING:
				a = encoder.get(2)
				b = encoder.get(3) # read the encoders
				# move up or down from the encoder a value
				if a > e2:
					game.up()
					#print("game up")
				elif a < e2:
					game.down()
					#print("game down")
				# move left or right from the encoder b value
				if b>e3:
					game.left()
					#print("game left")
				elif b < e3:
					game.right()
					#print("game right")
				#print(e2,e3,a,b)
				e2,e3=a,b
				
			sleep(0.1)
	finally:
		GPIO.cleanup()


if __name__ == "__main__":
	main()
