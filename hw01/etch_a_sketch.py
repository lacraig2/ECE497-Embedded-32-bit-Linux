#!/usr/bin/python

# By: Luke Craig
# Dr. Yoder
# ECE497 Embedded 32-bit Linux
# HW01

from curses import KEY_DOWN, KEY_UP, KEY_LEFT, KEY_RIGHT, curs_set, wrapper
from optparse import OptionParser
from math import log10

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
    return int(log10(n))+1

def main(stdscr):
    # parse command line options
    parser = OptionParser()
    parser.add_option("-n", dest="n", help="n size argument to game")
    parser.add_option("-m", dest="m", help="m size argument to game")
    options,args = parser.parse_args()

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

    # run main game
    while True:
        # print usage
        stdscr.addstr(0, 0, "Etch-a-sketch for ECE497-01 Embedded 32-bit Linux By: Luke Craig")
        stdscr.addstr(1, 0, "USE YOUR ARROW KEYS to move, c to clear, and q to quit.")
        stdscr.addstr(2, 0, str(game))
        stdscr.refresh()
        curs_set(0) # this just prevents a blinking cursor

        #take user input
        a = stdscr.getch()

        #react to user input appopriately with game logic
        if a == ord('q') or a == ord('Q'):
           break
        elif a == KEY_DOWN:
           game.down()
        elif a == KEY_UP:
           game.up()
        elif a == KEY_LEFT:
           game.left()
        elif a == KEY_RIGHT:
           game.right()
        elif a == ord('c') or a == ord('C'):
           game.clear()

# start GUI from curses
wrapper(main)
