#!/usr/bin/env python3


# Import serial library for Arduino communication
import serial

# Create serial object for Arduino
serial = serial.Serial('/dev/tty.usbserial', 9600)

