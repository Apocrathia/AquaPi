#!/usr/bin/env python

# AquaPi Main Orchestrator

# This script will launch the following functionality of AquaPi
# * Arduino Communication
# * Database Initialization
# * Web Backend

# Bring in the main aquapi class
import aquapi

# Bring in additional classes
import aquapi.config

def daemonize():
	# setup pidfile and all that crap
	print('Daemonize')
	
def help_message():
	print('Help')
	# Will make this more verbose later
	
def main():
	# Do some switch handling

	# read in config file
	config = aquapi.config.read('config.ini')

	# Launch the test method in the main class
	#aquapi.test('0.0.0.0', 80)
	print('Launching ' + config['name'])
	aquapi.test(config['host'], config['port'])

# as long as this script was launched directly
if __name__ == "__main__":
	main()
