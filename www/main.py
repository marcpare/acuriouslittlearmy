from config import *

from bottle import route, run, request, response
from bottle import mako_view as view

@route('/pushjob')
def get_pushjob():
	request_data = request.GET
	
	# push the job onto beanstalkd
	
	# return success code
	return request_data["type"]


@route('/')
@view('index')
def index():
	return {"root_url": ROOT_URL}

if ENVIRONMENT == "development":
	run(reloader=True, host=HOST, port=PORT)	
