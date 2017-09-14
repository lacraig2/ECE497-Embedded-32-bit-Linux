#!/usr/bin/env python3
# Read a TMP101 sensor

import smbus
import time
bus = smbus.SMBus(1)
address = 0x48
address2 = 0x4A

bus.write_byte_data(address,2,23)
bus.write_byte_data(address,3,27)
bus.write_byte_data(address2,2,23)
bus.write_byte_data(address2,3,27)
GPIO.setup("GPIO1_3", GPIo.

while True:
    temp = bus.read_byte_data(address, 0)
    temp2 = bus.read_byte_data(address2,0)
    print(str(temp)+" "+str(temp2),  end="\r")
    time.sleep(0.25)
