#!/usr/bin/env python3

# AquaPi WebUI Class

# get some system libraries
import os

# import main class
import aquapi

# import webserver
import flask, flask.views

# set a webui object
webui = flask.Flask(__name__)

# need a key for posts
webui.secret_key = "aquapi" # very insecure, change to md5

# simple dict of users
users = {'test': 'test'}

# setup pages
webui.add_url_rule('/', 
		view_func=Main.as_view('index'),
		methods=['GET', 'POST'])

webui.add_url_rule('/ledtest/', 
		view_func=LEDTest.as_view('ledtest'), 
		methods=['GET', 'POST'])

# views for each page containing code

# Front page: Login
class Main(flask.views.MethodView):
	def get(self):
		return flask.render_template('index.html')

	def post(self):
		# Define required fields
		required = ['username', 'passwd']
		# Make sure fields are present
		for r in required:
			if r not in flask.request.form:
				flask.flash("Error: {0} is required.".format(r))
				return flask.redirect(flask.url_for('index'))

		# Assign fields to variables
		username = flask.request.form['username']
		passwd = flask.request.form['passwd']

		# Verify username and password
		if users.get(username) == passwd:
			flask.session['username'] = username
		else:
			flask.flash("Username doesn't exist or incorrect password")

		return flask.redirect(flask.url_for('index'))

# overloads Flask's view method
class LEDTest(flask.views.MethodView):
	def get(self):
		# returns test.html in the 'templates' folder
		return flask.render_template('ledtest.html')

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
		# finally
		return flask.redirect(flask.url_for('ledtest'))

def startServer(host="127.0.0.1", port=8080, debug=True):
	webui.debug = debug

	# start the server.
	webui.run(host, port)
