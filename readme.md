# AquaPi
======

The aim of this project is to utilize the Raspberry Pi as a platform for an aquarium controller suitable for large reef and aquaponic systems.

This project is still in an embryonic state, and needs help, as I'm not a great developer.

The project's home page is located at [aquapi.org][aquapi.org].

Bug tracking is on [Google Code][googleissues].

Loosely based upon rob's project at [thereefuge.com.au][reefuge]. Unlike rob's project, which relied heavily upon the Raspberry Pi's digial-only GPIO, this project aims to take advantage of the Arduino's analog/digital capabilities, and interface directly with a Python-based backend. The GPIO can then be used later for an external LCD display.

------

## Goals
  * Monitor temperature, pH, ORP, and salinity
  * Control water levels
  * Dosing control
  * Lighting control
  * Feeder control
  * Air pump control

## Requirements:
  * Python 2.5 or higher
  * An Arduino compatible microcontroller with at least 14KB of flash memory
  * Flask 0.10
  * arduino-python 0.2

## Installation:
  * **AquaPi is nowhere near ready**
  * Run the following to execute the setup script (as root or with sudo): 
```
bash <(curl -s https://raw.github.com/Apocrathia/AquaPi/master/tools/setup.sh)
```	
  * Upload the sketch `avr/src/sketch.ino` to your controller (The script doesn't do this [yet]).

## AquaPi utilizes the following projects
  * [Flask][flask]
  * [jQuery][jquery]
  * [Inotool][inotool]
  * [pySerial][pyserial]
  * [arduino-python][arduinoapi]
  * And some borrowed code from [SickBeard][sickbeard]

[aquapi.org]: http://aquapi.org
[reefuge]: http://www.thereefuge.com.au/threads/raspberry-pi-tank-monitor-project.3475
[sickbeard]: http://sickbeard.com
[flask]: http://flask.pocoo.org/
[inotool]: http://inotool.org
[jquery]: http://jquery.com
[pyserial]: http://pyserial.sourceforge.net/
[arduinoapi]: https://github.com/thearn/Python-Arduino-Command-API
[buildarduino]: http://playground.arduino.cc/BuildArduino/Py
[googleissues]: http://code.google.com/p/aquapi/issues/list
[googlenewissue]: http://code.google.com/p/aquapi/issues/entry
