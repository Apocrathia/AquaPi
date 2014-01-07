#!/usr/bin/env python3

# AquaPi Main Class

# get some system libraries
import os

# import local libraries
import aquapi.webui

# Import arduino API
from Arduino import Arduino

# need an object that can be referenced from everywhere
global arduino
arduino = Arduino('9600')

def test(host="127.0.0.1", port=8080):
	# set pin 13 to output, since that's the one we're using in the test
	arduino.pinMode(13, "OUTPUT")

	# start the server.
	webui.startServer(host, port)
