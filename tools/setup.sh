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

# we need an announce function with a bunch of lines and shit
function announce {
	echo "=================================================="
	echo $1
	echo "=================================================="
}

# pull in the latest source from GitHub
announce "Let's pull in the source code..."
git clone https://github.com/Apocrathia/AquaPi.git

# dependencies
announce "Now, we're just going to install some dependencies..."

# fix pip (Just in case you get the same error)
# (really no harm in updating it regardless)
pip install setuptools --no-use-wheel --upgrade

# install flask
pip install flask

# install the arduino api
pip install arduino-python

# pip install inotool
pip install ino

# upload the sketch!
announce "Getting ready to upload the Arduino sketch..."
while true; do
	read -p 'Is your Arduino connected?' yn
	case $yn in
	    [Yy]* ) cd AquaPi/avr/api/; ino upload; break;;
	    [Nn]* ) echo "Please connect your Arduino!"; sleep 5;;
	    * ) echo "Please answer yes or no.";;
	esac
done

# hopefully this worked.
announce "Looks like we're good! Now run the AquaPi.py script to start using AquaPi!"

# done
exit