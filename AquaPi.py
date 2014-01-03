#!/usr/bin/env python

# AquaPi Main Orchestrator

# This script will launch the following functionality of AquaPi
# * Arduino Communication
# * Database Initialization
# * Web Backend

# A lot of this is blantantly ripped from SickBeard
# simply because of how awesome SickBeard is. As the project matures
# I'm sure the code will morph into it's own thing, but it's a
# perfect start to build the application around.

# bring in system libraries
import sys
import subprocess
import os

# we need this to read out config file
import configparser

# We're going to 
# make sure that the python is recent enough
if sys.version_info < (3, 0):
	sys.exit("Please update your Python environment to 3.0 or greater")

def main():
	# wait, did we get some parameters?
	# What about any configuration options?
	config = read_config('config.ini')
	NAME = config['General']['name']
	HOST = config['Server']['hostname']
	PORT = config['Server']['port']

	subprocess.call(['manage.py', "{}:{}".format(HOST,PORT)])

def read_config(configfile):
	config = configparser.ConfigParser()
	config.read(configfile)
	return config

# as long as this script was launched directly
if __name__ == "__main__":
	main()
