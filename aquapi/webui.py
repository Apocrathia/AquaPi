#!/usr/bin/env python

# AquaPi WebUI Class

# import additional classes
import aquapi.settings

# import webserver
import flask, flask.views

# import views
from aquapi.login import Login
from aquapi.ledtest import LEDTest
from aquapi.main import Main

# set a webui object
webui = flask.Flask(__name__)

# bring in our api key
webui.secret_key = aquapi.settings.secret_key

# setup pages (Has to be done after classes are defined)
webui.add_url_rule('/', 
		view_func=Main.as_view('index'),
		methods=['GET'])

webui.add_url_rule('/<page>/', 
		view_func=Main.as_view('page'),
		methods=['GET'])

webui.add_url_rule('/login/', 
		view_func=Login.as_view('login'),
		methods=['GET', 'POST'])

webui.add_url_rule('/ledtest/', 
		view_func=LEDTest.as_view('ledtest'), 
		methods=['GET', 'POST'])

webui.add_url_rule('/temptest/', 
		view_func=TempTest.as_view('temptest'), 
		methods=['GET'])

@webui.errorhandler(404)
def page_not_found(error):
	return flask.render_template('404.html'), 404

# Start Server function
def startServer(host="127.0.0.1", port=8080, debug=True):
	webui.debug = debug

	# start the server.
	webui.run(host, port)
