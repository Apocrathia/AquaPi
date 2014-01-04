#!/bin/bash

# This script will ensure that the proper packages are
# installed on your system for the AquaPi application.
# These requirements include
# * The latest AquaPi source
# * Python (Obviously)
# * Flask
# * arduino-python

# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "I'm sorry dave. I'm afraid I can't do that."
   exit
fi

# pull in the latest source from GitHub
git clone https://github.com/Apocrathia/AquaPi.git

# fix pip (Just in case you get the same error)
# (really no harm in updating it regardless)
pip install setuptools --no-use-wheel --upgrade

# install flask
pip install flask

# install the arduino api
pip install python-arduino