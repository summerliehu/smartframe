# -*- coding: utf-8 -*-
#smartframe.py

from werkzeug.wrappers import Response, Request
from werkzeug.serving import run_simple
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect



class Route:
    def __init__(self):
        self.url_map = Map([])
        self.endpoint_dict = {}

    def __call__(self, rules, endpoint_value=0):
        def wrapper(func):
            endpoint = endpoint_value
            if not endpoint:
                endpoint = func.__name__
            self.url_map.add(Rule(rules, endpoint=endpoint))
            self.endpoint_dict[endpoint] = func
            return func
        return wrapper

class Application(object):

    def __init__(self):
        self.route = Route()

    def __call__(self, environ, start_response):
        return self.application(environ, start_response)

    @Request.application
    def application(self,request):
        urls = self.bind_to_environ(request.environ)
        try:
            endpoint, args = urls.match()
        except Exception, e:
            return Response(str(e))
        return self.route.endpoint_dict[endpoint](request)

    def bind_to_environ(self, env):
        return self.route.url_map.bind_to_environ(env)

app = Application()

@app.route('/', 'index')
def index(request):
    urls = app.bind_to_environ(request.environ)
    endpoint = urls.match()[0]
    return Response("Welcome to %s!" % endpoint)

@app.route('/id/<int:id>')
def id(request):
    urls = app.bind_to_environ(request.environ)
    values = urls.match()[1]
    return Response("id is: %s" % values["id"])

@app.route('/current_url/', 'current_url')
def current_url(request):
    urls = app.bind_to_environ(request.environ)
    url = urls.build("current_url")
    return Response("current url is %s" % url)


run_simple('localhost', 8000, app, use_reloader = True)
