#!/usr/bin/env python

# Import arduino API
from Arduino import Arduino

# needed for some of the sleep functions
import time

def connect(baud='9600'):
	board = Arduino(baud)
	return board

# blink an LED
def blink(self, led_pin):
    while True:
        self.digitalWrite(led_pin, "HIGH")
        print self.digitalRead(led_pin)  # confirm HIGH (1)
        time.sleep(1)
        self.digitalWrite(led_pin, "LOW")
        print self.digitalRead(led_pin)  # confirm HIGH (0)
        time.sleep(1)

