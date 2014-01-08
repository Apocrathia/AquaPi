#!/usr/bin/env python

# AquaPi Login View

# import local modules
import aquapi.settings

# import webserver
import flask, flask.views

# Front page: Login
class Main(flask.views.MethodView):
	def get(self):
		return flask.render_template('index.html')

	def post(self):
		# Check logout
		if 'logout' in flask.request.form:
			flask.session.pop('username', None)
			return flask.redirect(flask.url_for('index'))
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
		if username in aquapi.settings.users and aquapi.settings.users[username] == passwd:
			flask.session['username'] = username
		else:
			flask.flash("Username doesn't exist or incorrect password")

		return flask.redirect(flask.url_for('index'))
