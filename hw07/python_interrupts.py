
#!/usr/bin/env python3

def update(channel):
	# main logic for moving the cursor
	GPIO.output("GP1_4",GPIO.input("GP1_3"))
	

def main(stdsc):

	# set up PAUSE pin for clear functionality
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