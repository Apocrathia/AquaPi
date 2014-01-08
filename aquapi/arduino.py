#!/usr/bin/env python

# AquaPi arduino module

# Import arduino API
from Arduino import Arduino

# need an object that can be referenced from everywhere
global arduino
arduino = Arduino('9600')

def ledtest(pin=13):
	# set pin 13 to output, since that's the one we're using in the test
	arduino.pinMode(pin, "OUTPUT")
