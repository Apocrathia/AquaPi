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

def read_config(configfile = 'config.ini'):
	print('Reading configuration file')
	# Do stuff
	config = ConfigParser.ConfigParser()
	config.read(configfile)

	# Case statement for attribute selector
	return {
		'name': str(config.get('General','name')),
		'host': str(config.get('Server','host')),
		'port': int(config.get('Server','port')),
	}
	
def help_message():
	print('Help')
	# Will make this more verbose later
	
def main():
	# Do some switch handling

	# read in config file
	config = read_config('config.ini')

	# Launch the test method in the main class
	#aquapi.test('0.0.0.0', 80)
	print('Launching ' + config['name'])
	aquapi.test(config['host'], config['port'])

# as long as this script was launched directly
if __name__ == "__main__":
	main()
