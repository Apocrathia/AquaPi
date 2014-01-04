#!/usr/bin/env python

# Import arduino API
from Arduino import Arduino

# needed for some of the sleep functions
import time

global controller

def __init__():
	controller.connect('')

def connect(baud='9600'):
	controller = Arduino(baud)
	
def initalize(pin, mode='OUTPUT'):
	controller.pinMode(pin, mode)

# blink an LED
def blink():
    while True:
        controller.digitalWrite(led_pin, "HIGH")
        print controller.digitalRead(led_pin)  # confirm HIGH (1)
        time.sleep(1)
        controller.digitalWrite(led_pin, "LOW")
        print controller.digitalRead(led_pin)  # confirm HIGH (0)
        time.sleep(1)

