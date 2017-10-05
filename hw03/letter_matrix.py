#!/usr/bin/env python3
# Write an 8x8 Red/Green LED matrix
# https://www.adafruit.com/product/902

import smbus
from time import sleep
from random import randint

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

	def set_pixel(self, x,y,color):
		self.matrix_red[x][y] = color[0]
		self.matrix_green[x][y] = color[1]
		self.update()

	def set_row(self, x, color):
		for i in range(len(self.matrix_red[0])):
			self.set_pixel(x,i, color)

	def set_col(self, x,color):
		for i in range(len(self.matrix_red)):
			self.set_pixel(i,x,color)

	def color(self, color):
		for i in range(len(self.matrix_red)):
			for j in range(len(self.matrix_red)):
				self.set_pixel(i,j, color)

	def clear(self):
		self.color(BLACK)

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

def main():
	bus = smbus.SMBus(1)  # Use i2c bus 1
	matrixAddr = 0x70         # Use address 0x70
	matrix = Matrix(8, matrixAddr, bus)
	matrix.color(matrix.BLACK)
	colors = [matrix.BLACK, matrix.YELLOW, matrix.RED, matrix.GREEN]
	while True:
		matrix.set_pixel(randint(0,7), randint(0,7), colors[randint(1,3)])
		sleep(0.005)
if __name__ == "__main__":
	main()
