#!/usr/bin/env python3

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

# We're going to 
# make sure that the user is running Python3
if sys.version_info < (3, 0):
	sys.exit("Please update your Python environment to 2.5 or greater")

def main():


# as long as this script was launched directly
if __name__ == "__main__":
	main()
