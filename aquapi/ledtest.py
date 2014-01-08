#!/usr/bin/env python

# AquaPi LEDTest View

# import main class
import aquapi

# import webserver
import flask, flask.views

# Import utilities
import aquapi.utils

# LED Test Page
class LEDTest(flask.views.MethodView):
	@aquapi.utils.login_required
	def get(self):
		# returns test.html in the 'templates' folder
		return flask.render_template('ledtest.html')

	@aquapi.utils.login_required
	def post(self):
		# we want to execute the code
		# if the on button was pushed
		if flask.request.form['btn'] == 'On':
			# flash the message in the page
			flask.flash("Turning the lights On")
			# and turn the pin on
			aquapi.arduino.digitalWrite(13, "HIGH")
		# or if the off button was pushed
		elif flask.request.form['btn'] == 'Off':
			# show a message
			flask.flash("Turning the lights Off")
			# connect to the arduino
			aquapi.arduino.digitalWrite(13, "LOW")
		# This doesn't really do anything yet
		elif flask.request.form['btn'] == 'Toggle':
			# Show a message
			flask.flash("Toggling lights")
			# read status
			# reverse status
		# finally
		return flask.redirect(flask.url_for('ledtest'))