#!/usr/bin/env python

# AquaPi Main Orchestrator

# This script will launch the following functionality of AquaPi
# * Arduino Communication
# * Database Initialization
# * Web Backend

# use the config parser class
import ConfigParser

# Bring in the main aquapi class
import aquapi

def daemonize():
	# setup pidfile and all that crap
	print('Daemonize')

def read_config(configfile):
	print('Reading configuration file')
	# Do stuff
	
def help_message():
	print('Help')
	# Will make this more verbose later
	
def main():
	# read in config file
	config = ConfigParser.ConfigParser()
	config.read('config.ini')

	host = str(config.get('Server','hostname'))
	port = int(config.get('Server','port'))

	# Launch the test method in the main class
	#aquapi.test('0.0.0.0', 80)
	aquapi.test(host, port)

# as long as this script was launched directly
if __name__ == "__main__":
	main()
