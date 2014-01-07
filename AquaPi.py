#!/usr/bin/env python3

# AquaPi Main Orchestrator

# This script will launch the following functionality of AquaPi
# * Arduino Communication
# * Database Initialization
# * Web Backend

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
	# Launch the test method in the main class
	aquapi.test('0.0.0.0', 80)

# as long as this script was launched directly
if __name__ == "__main__":
	main()
