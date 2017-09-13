#!/usr/bin/python

# By: Luke Craig
# Dr. Yoder
# ECE497 Embedded 32-bit Linux
# HW02

import Adafruit_BBIO.GPIO as GPIO
from time import sleep

# pairs in the form (OUTPUT, INPUT, STATE)
# state takes care of which are pull up and pull down
GPIOs = [("GP1_3","GP0_3", GPIO.HIGH), ("GP1_4","GP0_4", GPIO.LOW), ("RED", "GP0_5", GPIO.HIGH),("GREEN","GP0_6", GPIO.LOW)]

def main():
	try:
		# set up GPIOs as appopriate
		for i in GPIOs:
			GPIO.setup(i[1], GPIO.IN);
			GPIO.setup(i[0], GPIO.OUT);

		# main program loop
		while True:
			# set as appopriate for each GPIO
			for i in GPIOs:
				GPIO.output(i[0], GPIO.HIGH if GPIO.input(i[1]) != i[2] else GPIO.LOW);
			# sleep for 100 ms
			sleep(0.1)
	finally:
		GPIO.cleanup()

if __name__ == "__main__":
    main()