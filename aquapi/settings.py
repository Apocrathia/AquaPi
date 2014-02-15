#!/usr/bin/env python

# AquaPi Settings View

# import Flask
import flask, flask.views

# need a key for posts
secret_key = "714c2e212a824bfa2c80398d873232be" # md5 for 'aquapi'

# simple dict of users
users = {'test': 'test'}

# Front page: Login
class Settings(flask.views.MethodView):
	def get(self):
		pass

	def post(self):
		pass