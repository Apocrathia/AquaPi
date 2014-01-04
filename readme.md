AquaPi
======

The aim of this project is to utilize the Raspberry Pi as
a platform for an aquarium controller suitable for large
reef and aquaponic systems.

This project is still in the planning phase, as I am currently
developing requirements and sourcing parts.

The project's home page is located at [aquapi.org][aquapi.org]

Bug tracking is on [Google Code][googleissues].

Loosely based upon rob's project at [thereefuge.com.au][reefuge]

Goals
  * Monitor temperature, pH, ORP, and salinity
  * Control water levels
  * Dosing control
  * Lighting control
  * Feeder control
  * Air intake control

Ideas
  * Setup script for easy deployment
  * Use jQuery graphs instead of RRD

Requirements:
  * Python 3 or higher
  * pyserial 2.6 or higher
  * An Arduino compatible microcontroller with at least 14KB of flash memory

Installation:
  * AquaPi is nowhere near ready
  * run the following: ```bash 
bash <(curl -s https://raw.github.com/Apocrathia/AquaPi/master/tools/setup.sh)
```

AquaPi utilizes the following projects
  * [Flask][flask]
  * [jQuery][jquery]
  * [Ino][inotool]
  * [pySerial][pyserial]
  * [arduino-python][arduinoapi]
  * [And some borrowed code from SickBeard][sickbeard]

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
