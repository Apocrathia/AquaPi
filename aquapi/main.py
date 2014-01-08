#!/usr/bin/env python

# AquaPi Main View

import os

# import webserver
import flask, flask.views

# Front page
class Main(flask.views.MethodView):
	def get(self, page = 'index'):
		page += ".html"
		if os.path.isfile('aquapi/templates/' + page):
			return flask.render_template(page)
		else:
			flask.abort(404)
