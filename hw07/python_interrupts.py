
#!/usr/bin/env python
import Adafruit_BBIO.GPIO as GPIO
from time import sleep	


def update(channel):
	# just follow the pin
	GPIO.output("GP1_4",GPIO.input("GP1_3"))
	
def main():

	# set up pins for clear functionality and callback structure
	GPIO.setup("GP1_3", GPIO.IN)
	GPIO.setup("GP1_4", GPIO.OUT)
	GPIO.add_event_detect("GP1_3", GPIO.BOTH, callback=update)

	# sleep  
	try:
		while True:
			sleep(100)
	finally:
		GPIO.cleanup()

if __name__ == "__main__":
	main()