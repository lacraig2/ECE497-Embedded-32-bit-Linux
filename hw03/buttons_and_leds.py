#!/usr/bin/python

# By: Luke Craig
# Dr. Yoder
# ECE497 Embedded 32-bit Linux
# HW02

import Adafruit_BBIO.GPIO as GPIO
from time import sleep

GPIOs = [("GP1_3","GP0_3", GPIO.HIGH), ("GP1_4","GP0_4", GPIO.LOW), ("RED", "GP0_5", GPIO.HIGH),("GREEN","GP0_6", GPIO.LOW)]

def main():
	try:
		for i in GPIOs:
			#print("input "+i[1])
			GPIO.setup(i[1], GPIO.IN);
			#print("output "+ i[0])
			GPIO.setup(i[0], GPIO.OUT);
		a = GPIO.LOW
		while True:
			a = GPIO.LOW if a == GPIO.HIGH else GPIO.HIGH
			#print(GPIO.input("GP0_3"), GPIO.input("GP0_4"), GPIO.input("GP0_5"), GPIO.input("GP0_6"))
			for i in GPIOs:
				GPIO.output(i[0], GPIO.HIGH if GPIO.input(i[1]) != i[2] else GPIO.LOW);
				i#print(i[1] + "is set to " + str(GPIO.input(i[1])))
			#print("Setting all to " + str(a))
			sleep(0.1)
	finally:
		GPIO.cleanup()				
if __name__ == "__main__":
    main()


