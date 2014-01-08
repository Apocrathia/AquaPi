#!/usr/bin/env python

# AquaPi WebUI Class

# get some system libraries
import os
import functools

# import main class
import aquapi

# import additional classes
import aquapi.settings

# import webserver
import flask, flask.views

# import views
from aquapi.login import Main
from aquapi.ledtest import LEDTest

# set a webui object
webui = flask.Flask(__name__)

webui.secret_key = aquapi.settings.secret_key

# setup pages (Has to be done after classes are defined)
webui.add_url_rule('/', 
		view_func=Main.as_view('login'),
		methods=['GET', 'POST'])

webui.add_url_rule('/ledtest/', 
		view_func=LEDTest.as_view('ledtest'), 
		methods=['GET', 'POST'])

# Start Server function
def startServer(host="127.0.0.1", port=8080, debug=True):
	webui.debug = debug

	# start the server.
	webui.run(host, port)
