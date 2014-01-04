#!/usr/bin/env python

# AquaPi Main Class

# get some system libraries
import os

# import webserver to test
import flask, flask.views

# import arduino class
import controller

# overloads Flask's view method
class View(flask.views.MethodView):
	def get(self):
		# returns test.html in the 'templates' folder
		return flask.render_template('test.html')
		
	def post(self):
		# we want to execute the code
		result = eval(flask.request.form['input'])
		# display the result
		flask.flash(result)
		# and refresh the page
		return self.get()

def test():
	# instantiate a new arduino
	arduino = controller.connect('9600')

	# set a webui object
	webui = flask.Flask(__name__)
	
	# need a key for posts
	webui.secret_key = "aquapi"
	
	# set the main page
	webui.add_url_rule('/', view_func=View.as_view('main'), methods=['GET', 'POST'])
	
	webui.debug = True
	
	# start the server.
	webui.run('0.0.0.0', 80)
