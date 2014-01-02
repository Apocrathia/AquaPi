#!/bin/bash

# This script will ensure that the proper packages are
# installed on your system for the AquaPi application.
# These requirements include
# * The latest AquaPi source
# * Python
# * CherryPy
# * Cheetah
# * pyserial
# * arduino-python

# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "I'm sorry dave. I'm afraid I can't do that."
   exit
fi

# pull make sure that this is the latest source from GitHub
pwd
cd ..
pwd
git pull;
