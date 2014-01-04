#!/usr/bin/env python

# AquaPi Main Class

# get some system libraries
import os

# import webserver to test
import flask, flask.views

# import arduino class
#from controller import controller
# Import arduino API
from Arduino import Arduino

# need an object that can be referenced from everywhere
global arduino

# overloads Flask's view method
class View(flask.views.MethodView):
	def get(self):
		# returns test.html in the 'templates' folder
		return flask.render_template('test.html')
		
	def post(self):
		# we want to execute the code
		if flask.request.form['btn'] == 'On':
			flask.flash("Turning the lights On")
			arduino = Arduino('9600')
			arduino.digitalWrite(13, "HIGH")
		elif flask.request.form['btn'] == 'Off':
			flask.flash("Turning the lights Off")
			arduino = Arduino('9600')
			arduino.digitalWrite(13, "LOW")
		# finally
		return self.get()

def test(host="127.0.0.1", port=8080):
	# instantiate a new arduino
	arduino = Arduino('9600')
	
	# set pin 13 to output, since that's the one we're using in the test
	arduino.pinMode(13, "OUTPUT")

	# set a webui object
	webui = flask.Flask(__name__)
	
	# need a key for posts
	webui.secret_key = "aquapi"
	
	# set the main page
	webui.add_url_rule('/', view_func=View.as_view('main'), methods=['GET', 'POST'])
	
	webui.debug = True
	
	# start the server.
	webui.run(host, port)
