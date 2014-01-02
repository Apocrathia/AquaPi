#!/usr/bin/env python

# AquaPi Main Orchestrator

# This script will launch the following functionality of AquaPi
# * Arduino Communication
# * Database Initialization
# * Web Server

# A lot of this is blantantly ripped from SickBeard
# simply because of how awesome SickBeard is. As the project matures
# I'm sure the code will morph into it's own thing, but it's a
# perfect start to build the application around.

# bring in system libraries
import sys

# make sure that the user is running Python3
if sys.version_info < (2, 5):
	sys.exit("Please update your Python environment to 2.5 or greater")

# Bring in the web template framework	
try:
    import Cheetah
    if Cheetah.Version[0] != '2':
        raise ValueError
except ValueError:
    sys.exit("Sorry, requires Python module Cheetah 2.1.0 or newer.")
except:
    sys.exit("The Python module Cheetah is required")
	
# Here are libraries which will allow AquaPi to communicate with the host
import locale
import os
import threading
import time
import signal
import traceback
import getopt

# # Import serial library for raw Arduino communication
from lib.serial import serial
# # Create serial object for Arduino
# serial = serial.Serial('/dev/tty.usbserial', 9600)

# Import Arduino API Library
from .lib.Arduino import Arduino
import time

# Finally, import the AquaPi library itself
import aquapi

from aquapi import db
from aquapi import logger
from aquapi.version import AQUAPI_VERSION

from aquapi.webserveInit import initWebServer

from lib.configobj import ConfigObj

signal.signal(signal.SIGINT, aquapi.sig_handler)
signal.signal(signal.SIGTERM, aquapi.sig_handler)


# SickBeard some really awesome code to start with

# This is the daemonize method
# This allows us to run AquaPi as a background process
# which can be supervised from init or systemd
def daemonize():
    """
    Fork off as a daemon
    """

    # pylint: disable=E1101
    # Make a non-session-leader child process
    try:
        pid = os.fork()  # @UndefinedVariable - only available in UNIX
        if pid != 0:
            os._exit(0)
    except OSError as e:
        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)

    os.setsid()  # @UndefinedVariable - only available in UNIX

    # Make sure I can read my own files and shut out others
    prev = os.umask(0)
    os.umask(prev and int('077', 8))

    # Make the child a session-leader by detaching from the terminal
    try:
        pid = os.fork()  # @UndefinedVariable - only available in UNIX
        if pid != 0:
            os._exit(0)
    except OSError as e:
        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)

    # Write pid
    if aquapi.CREATEPID:
        pid = str(os.getpid())
        logger.log(u"Writing PID: " + pid + " to " + str(aquapi.PIDFILE))
        try:
            file(aquapi.PIDFILE, 'w').write("%s\n" % pid)
        except IOError as e:
            error_msg = "Unable to write PID file: " + aquapi.PIDFILE + " Error: " + str(e.strerror) + " [" + str(e.errno) + "]"
            logger.log(u"" + error_msg, logger.ERROR)
            sys.exit(error_msg)

    # Redirect all output
    sys.stdout.flush()
    sys.stderr.flush()

    devnull = getattr(os, 'devnull', '/dev/null')
    stdin = file(devnull, 'r')
    stdout = file(devnull, 'a+')
    stderr = file(devnull, 'a+')
    os.dup2(stdin.fileno(), sys.stdin.fileno())
    os.dup2(stdout.fileno(), sys.stdout.fileno())
    os.dup2(stderr.fileno(), sys.stderr.fileno())
	
# help message call
def help_message():
    """
    print help message for commandline options
    """
    help_msg = "\n"
    help_msg += "Usage: " + aquapi.MY_FULLNAME + " <option> <another option>\n"
    help_msg += "\n"
    help_msg += "Options:\n"
    help_msg += "\n"
    help_msg += "    -h          --help              Prints this message\n"
    help_msg += "    -q          --quiet             Disables logging to console\n"
    help_msg += "                --nolaunch          Suppress launching web browser on startup\n"
    help_msg += "    -d          --daemon            Run as double forked daemon (includes options --quiet --nolaunch)\n"
    help_msg += "                --pidfile=<path>    Combined with --daemon creates a pidfile (full path including filename)\n"
    help_msg += "    -p <port>   --port=<port>       Override default/configured port to listen on\n"
    help_msg += "                --datadir=<path>    Override folder (full path) as location for\n"
    help_msg += "                                    storing database, configfile, cache, logfiles \n"
    help_msg += "                                    Default: " + aquapi.PROG_DIR + "\n"
    help_msg += "                --config=<path>     Override config filename (full path including filename)\n"
    help_msg += "                                    to load configuration from \n"
    help_msg += "                                    Default: config.ini in " + aquapi.PROG_DIR + " or --datadir location\n"

    return help_msg
	
# Finally start the application
def main():
    """
    TV for me
    """

    # do some preliminary stuff
    aquapi.MY_FULLNAME = os.path.normpath(os.path.abspath(__file__))
    aquapi.MY_NAME = os.path.basename(aquapi.MY_FULLNAME)
    aquapi.PROG_DIR = os.path.dirname(aquapi.MY_FULLNAME)
    aquapi.DATA_DIR = aquapi.PROG_DIR
    aquapi.MY_ARGS = sys.argv[1:]
    aquapi.DAEMON = False
    aquapi.CREATEPID = False

    aquapi.SYS_ENCODING = None

    try:
        locale.setlocale(locale.LC_ALL, "")
        aquapi.SYS_ENCODING = locale.getpreferredencoding()
    except (locale.Error, IOError):
        pass

    # For OSes that are poorly configured I'll just randomly force UTF-8
    if not aquapi.SYS_ENCODING or aquapi.SYS_ENCODING in ('ANSI_X3.4-1968', 'US-ASCII', 'ASCII'):
        aquapi.SYS_ENCODING = 'UTF-8'

    if not hasattr(sys, "setdefaultencoding"):
        reload(sys)

    try:
        # pylint: disable=E1101
        # On non-unicode builds this will raise an AttributeError, if encoding type is not valid it throws a LookupError
        sys.setdefaultencoding(aquapi.SYS_ENCODING)
    except:
        sys.exit("Sorry, you MUST add the AquaPi folder to the PYTHONPATH environment variable\n" +
            "or find another way to force Python to use " + aquapi.SYS_ENCODING + " for string encoding.")

    # Need console logging for AquaPi.py
    consoleLogging = (not hasattr(sys, "frozen")) or (aquapi.MY_NAME.lower().find('-console') > 0)

    # Rename the main thread
    threading.currentThread().name = "MAIN"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hfqdp::", ['help', 'forceupdate', 'quiet', 'nolaunch', 'daemon', 'pidfile=', 'port=', 'datadir=', 'config=', 'noresize'])  # @UnusedVariable
    except getopt.GetoptError:
        sys.exit(help_message())

    forceUpdate = False
    forcedPort = None
    noLaunch = False

    for o, a in opts:

        # Prints help message
        if o in ('-h', '--help'):
            sys.exit(help_message())

        # Disables logging to console
        if o in ('-q', '--quiet'):
            consoleLogging = False

        # Suppress launching web browser
        # Needed for OSes without default browser assigned
        # Prevent duplicate browser window when restarting in the app
        if o in ('--nolaunch',):
            noLaunch = True

        # Run as a double forked daemon
        if o in ('-d', '--daemon'):
            aquapi.DAEMON = True
            # When running as daemon disable consoleLogging and don't start browser
            consoleLogging = False
            noLaunch = True

        # Write a pidfile if requested
        if o in ('--pidfile',):
            aquapi.CREATEPID = True
            aquapi.PIDFILE = str(a)

            # If the pidfile already exists, aquapi may still be running, so exit
            if os.path.exists(aquapi.PIDFILE):
                sys.exit("PID file: " + aquapi.PIDFILE + " already exists. Exiting.")

        # Override default/configured port
        if o in ('-p', '--port'):
            try:
                forcedPort = int(a)
            except ValueError:
                sys.exit("Port: " + str(a) + " is not a number. Exiting.")

        # Specify folder to use as data dir (storing database, configfile, cache, logfiles)
        if o in ('--datadir',):
            aquapi.DATA_DIR = os.path.abspath(a)

        # Specify filename to load the config information from
        if o in ('--config',):
            aquapi.CONFIG_FILE = os.path.abspath(a)

        # Prevent resizing of the banner/posters even if PIL is installed
        if o in ('--noresize',):
            aquapi.NO_RESIZE = True

    # The pidfile is only useful in daemon mode, make sure we can write the file properly
    if aquapi.CREATEPID:
        if aquapi.DAEMON:
            pid_dir = os.path.dirname(aquapi.PIDFILE)
            if not os.access(pid_dir, os.F_OK):
                sys.exit("PID dir: " + pid_dir + " doesn't exist. Exiting.")
            if not os.access(pid_dir, os.W_OK):
                sys.exit("PID dir: " + pid_dir + " must be writable (write permissions). Exiting.")

        else:
            if consoleLogging:
                sys.stdout.write("Not running in daemon mode. PID file creation disabled.\n")

            aquapi.CREATEPID = False

    # If they don't specify a config file then put it in the data dir
    if not aquapi.CONFIG_FILE:
        aquapi.CONFIG_FILE = os.path.join(aquapi.DATA_DIR, "config.ini")

    # Make sure that we can create the data dir
    if not os.access(aquapi.DATA_DIR, os.F_OK):
        try:
            os.makedirs(aquapi.DATA_DIR, 0o744)
        except os.error:
            sys.exit("Unable to create data directory: " + aquapi.DATA_DIR + " Exiting.")

    # Make sure we can write to the data dir
    if not os.access(aquapi.DATA_DIR, os.W_OK):
        sys.exit("Data directory: " + aquapi.DATA_DIR + " must be writable (write permissions). Exiting.")

    # Make sure we can write to the config file
    if not os.access(aquapi.CONFIG_FILE, os.W_OK):
        if os.path.isfile(aquapi.CONFIG_FILE):
            sys.exit("Config file: " + aquapi.CONFIG_FILE + " must be writeable (write permissions). Exiting.")
        elif not os.access(os.path.dirname(aquapi.CONFIG_FILE), os.W_OK):
            sys.exit("Config file directory: " + os.path.dirname(aquapi.CONFIG_FILE) + " must be writeable (write permissions). Exiting")

    os.chdir(aquapi.DATA_DIR)

    if consoleLogging:
        sys.stdout.write("Starting up Sick Beard " + SICKBEARD_VERSION + "\n")
        if not os.path.isfile(aquapi.CONFIG_FILE):
            sys.stdout.write("Unable to find '" + aquapi.CONFIG_FILE + "' , all settings will be default!" + "\n")

    # Load the config and publish it to the aquapi package
    aquapi.CFG = ConfigObj(aquapi.CONFIG_FILE)

    # Initialize the config and our threads
    aquapi.initialize(consoleLogging=consoleLogging)

    aquapi.showList = []

    if aquapi.DAEMON:
        daemonize()

    # Use this PID for everything
    aquapi.PID = os.getpid()

    if forcedPort:
        logger.log(u"Forcing web server to port " + str(forcedPort))
        startPort = forcedPort
    else:
        startPort = aquapi.WEB_PORT

    if aquapi.WEB_LOG:
        log_dir = aquapi.LOG_DIR
    else:
        log_dir = None

    # aquapi.WEB_HOST is available as a configuration value in various
    # places but is not configurable. It is supported here for historic reasons.
    if aquapi.WEB_HOST and aquapi.WEB_HOST != '0.0.0.0':
        webhost = aquapi.WEB_HOST
    else:
        if aquapi.WEB_IPV6:
            webhost = '::'
        else:
            webhost = '0.0.0.0'

    try:
        initWebServer({
                      'port': startPort,
                      'host': webhost,
                      'data_root': os.path.join(aquapi.PROG_DIR, 'data'),
                      'web_root': aquapi.WEB_ROOT,
                      'log_dir': log_dir,
                      'username': aquapi.WEB_USERNAME,
                      'password': aquapi.WEB_PASSWORD,
                      'enable_https': aquapi.ENABLE_HTTPS,
                      'https_cert': aquapi.HTTPS_CERT,
                      'https_key': aquapi.HTTPS_KEY,
                      })
    except IOError:
        logger.log(u"Unable to start web server, is something else running on port: " + str(startPort), logger.ERROR)
        if aquapi.LAUNCH_BROWSER and not aquapi.DAEMON:
            logger.log(u"Launching browser and exiting", logger.ERROR)
            aquapi.launchBrowser(startPort)
        sys.exit("Unable to start web server, is something else running on port: " + str(startPort))

    # Build from the DB to start with
    logger.log(u"Loading initial show list")
    loadShowsFromDB()

    # Fire up all our threads
    aquapi.start()

    # Launch browser if we're supposed to
    if aquapi.LAUNCH_BROWSER and not noLaunch and not aquapi.DAEMON:
        aquapi.launchBrowser(startPort)

    # Start an update if we're supposed to
    if forceUpdate:
        aquapi.showUpdateScheduler.action.run(force=True)  # @UndefinedVariable

    # Stay alive while my threads do the work
    while (True):

        if aquapi.invoked_command:
            aquapi.invoked_command()
            aquapi.invoked_command = None

        time.sleep(1)

    return

if __name__ == "__main__":
    if sys.hexversion >= 0x020600F0:
        freeze_support()
    main()