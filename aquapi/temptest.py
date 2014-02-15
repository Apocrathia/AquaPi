#!/usr/bin/env python

# AquaPi TenoTest View

# import main class
import aquapi

# import webserver
import flask, flask.views

# Import utilities
import aquapi.utils

# Temp Test Page
class TempTest(flask.views.MethodView):
	@aquapi.utils.login_required
	def get(self):
		# get the temperature from pin a0
		
		# returns test.html in the 'templates' folder
		return flask.render_template('temptest.html')