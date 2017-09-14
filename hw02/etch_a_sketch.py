#!/usr/bin/python

# By: Luke Craig
# Dr. Yoder
# ECE497 Embedded 32-bit Linux
# HW02

from curses import KEY_DOWN, KEY_UP, KEY_LEFT, KEY_RIGHT, curs_set, wrapper
from optparse import OptionParser
from math import log10
import Adafruit_BBIO.GPIO as GPIO
from time import sleep
from sys import exit

GPIOs = {"GP0_3": GPIO.RISING, "GP0_4": GPIO.FALLING, "GP0_5": GPIO.RISING,"GP0_6": GPIO.FALLING}
game = None			 # see note on globals below
stdscr = None

class Game:
	def __init__(self, n, m=None):
		'''The initializer for the game sets up the initial position and the game board'''
		if m is None:
			m = n
		self.n = n
		self.m = m
		self.x = 0
		self.y = 0
		self.numspaces = num_spaces(self.n)
		self.board = [[" " for j in range(n)] for i in range(m)]
		self.live = True

	def __str__(self):
		'''This method returns the base string representation of the Game class.'''
		return "  "+" ".join([str(i).rjust(self.numspaces+1) for i in range(self.n)])+"\n"+ "\n".join([(str(i)+": ").rjust(2+self.numspaces)+(" ".rjust(self.numspaces+1)).join([self.board[i][j] for j in range(self.n)]) for i in range(self.m)])

	def up(self):
		'''Moves the position up and marks it. Thoughtful of bounds.'''
		self.x = self.x -1  if self.x > 0 else 0
		self.board[self.x][self.y] = 'X'

	def down(self):
		'''Moves the position down and marks it. Thoughtful of bounds'''
		self.x = self.x +1 if self.x < self.m-1 else self.m-1
		self.board[self.x][self.y] = 'X'
	
	def left(self):
		'''Moves the position left and marks it. Thoughtful of bounds'''
		self.y = self.y -1 if self.y > 0 else 0
		self.board[self.x][self.y] = 'X'
	
	def right(self):
		'''Moves the position right and marks it. Thoughtful of bounds'''
		self.y = self.y+1 if self.y < self.n -1 else self.n -1
		self.board[self.x][self.y] = 'X'
	
	def clear(self):
		'''Clears the board to default values'''
		self.board = [[" " for j in range(self.n)]for i in range(self.m)]

def num_spaces(n):
	'''Number of spaces required to print a number in decimal. Useful in printing out board.'''
	return int(log10(n))+1

'''
On globals:

Yes, these are globals. I use two. Game and screen.
I use game because I that has to be global in this context to be able to use a callback.
I use stdscr as a global because instead of using a while loop to update every 100 ms this
only calls update_screen when it needs to (on events). I think this is a better approach on th whole.
'''

def update_game(channel):
	# main logic for moving the cursor
	if channel == "GP0_3":
		game.up()
	elif channel == "GP0_4":
		game.left()
	elif channel == "GP0_5":
		game.down()
	elif channel == "GP0_6":
		game.right()
	elif channel == "PAUSE":
		game.clear()
	update_screen()

'''
Simple method to update the curses screen.
'''
def update_screen():
	stdscr.addstr(0, 0, "Etch-a-sketch for ECE497-01 Embedded 32-bit Linux By: Luke Craig")
	stdscr.addstr(1, 0, "USE YOUR GPIO Pins to move and PAUSE to clear.")
	stdscr.addstr(2, 0, str(game))
	stdscr.refresh()
	curs_set(0) # this just prevents a blinking cursor

def main(stdsc):
	# parse command line options
	parser = OptionParser()
	parser.add_option("-n", dest="n", help="n size argument to game")
	parser.add_option("-m", dest="m", help="m size argument to game")
	options,args = parser.parse_args()
	global stdscr
	global game
	stdscr = stdsc
	# clear screen
	stdscr.clear()

	# set up game with command line options
	if options.m and options.n:
		n = int(options.n)
		m = int(options.m)
		game = Game(n if n < 25 else 8, m if m < 25 else 8)
	elif options.n:
		n = int(options.n)
		game = Game(n if n < 25 else 8)
	else:
		game = Game(8,8) # default

	# set up PAUSE pin for clear functionality
	GPIO.setup("PAUSE", GPIO.IN)
	GPIO.add_event_detect("PAUSE", GPIO.BOTH, callback=update_game)

	# set up input pins
	for i in GPIOs:
		GPIO.setup(i, GPIO.IN)
		GPIO.add_event_detect(i, GPIOs[i],callback=update_game)

	update_screen()  

	# sleep  
	try:
		while game.live:
			sleep(100)
	finally:
		GPIO.cleanup()

# start GUI from curses
wrapper(main)
