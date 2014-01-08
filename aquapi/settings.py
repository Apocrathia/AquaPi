#!/usr/bin/env python

# AquaPi Settings View

# import Flask
import flask, flask.views

# need a key for posts
secret_key = "aquapi" # very insecure, change to md5

# simple dict of users
users = {'test': 'test'}

# Front page: Login
class Settings(flask.views.MethodView):
	def get(self):
		pass

	def post(self):
		pass