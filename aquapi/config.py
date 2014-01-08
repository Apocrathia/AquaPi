#!/usr/bin/env python

# AquaPi Configuration

# use the config parser class
import ConfigParser

def read(configfile = 'config.ini'):
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