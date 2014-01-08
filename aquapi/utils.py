#!/usr/bin/env python

# AquaPi Utilities Class

# get some system libraries
import functools

# import webserver
import flask, flask.views

# wrapper for login requirement
def login_required(method):
	@functools.wraps(method)
	def wrapper(*args, **kwargs):
		if 'username' in flask.session:
			return method(*args, **kwargs)
		else:
			flask.flash("A login is required to view this page")
			return flask.redirect(flask.url_for('index'))
	return wrapper