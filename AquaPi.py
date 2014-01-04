#!/usr/bin/env python

# AquaPi Main Orchestrator

# This script will launch the following functionality of AquaPi
# * Arduino Communication
# * Database Initialization
# * Web Backend

# Bring in the main aquapi class
import aquapi


def main():
	
	# Launch the test method in the main class
	aquapi.test('0.0.0.0', 80)

def read_config(configfile):
	print 'Reading configuration file'
	# Do stuff

# as long as this script was launched directly
if __name__ == "__main__":
	main()
