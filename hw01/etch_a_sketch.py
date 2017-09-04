#!/usr/bin/python

# By: Luke Craig
# Dr. Yoder
# ECE497 Embedded 32-bit Linux
# HW01
from curses import wrapper
from curses import KEY_DOWN, KEY_UP, KEY_LEFT, KEY_RIGHT, curs_set
from optparse import OptionParser

class Game:
    def __init__(self, n, m=None):
        if m is None:
            m = n
        self.n = n
        self.m = m
        self.x = 0
        self.y = 0
        self.board = [[" " for j in range(n)] for i in range(m)]
    def __str__(self):
        return "   "+" ".join([str(i) for i in range(self.n)])+"\n"+ "\n".join([str(i)+": "+" ".join([self.board[i][j] for j in range(self.n)]) for i in range(self.m)])
    def up(self):
        self.x = self.x -1  if self.x > 0 else 0
        self.board[self.x][self.y] = 'X'
    def down(self):
        self.x = self.x +1 if self.x < self.m-1 else self.m-1
        self.board[self.x][self.y] = 'X'
    def left(self):
        self.y = self.y -1 if self.y > 0 else 0
        self.board[self.x][self.y] = 'X'
    def right(self):
        self.y = self.y+1 if self.y < self.n -1 else self.n -1
        self.board[self.x][self.y] = 'X'
    def clear(self):
        self.board = [[" " for j in range(self.n)]for i in range(self.m)]

def main(stdscr):
        parser = OptionParser()
        parser.add_option("-n", dest="n", help="n size argument to game")
        parser.add_option("-m", dest="m", help="m size argument to game")
        options,args = parser.parse_args()
        stdscr.clear()
        if options.m and options.n:
            game = Game(int(options.n),int(options.m))
        elif options.n:
            game = Game(int(options.n))
        else:
            game = Game(8,8)
        while True:
            stdscr.addstr(0, 0, "Etch-a-sketch for ECE497-01 Embedded 32-bit Linux By: Luke Craig")
            stdscr.addstr(1, 0, "USE YOUR ARROW KEYS to move, c to clear, and q to quit.")
            stdscr.addstr(2, 0, str(game))
            stdscr.refresh()
            curs_set(0)
            a = stdscr.getch()
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
        print("THANKS FOR PLAYING!")

wrapper(main)
