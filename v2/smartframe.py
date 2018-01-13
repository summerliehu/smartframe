# -*- coding: utf-8 -*-
#smartframe.py

from werkzeug.wrappers import Response, Request
from werkzeug.serving import run_simple
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect

url_map = Map([
    Rule('/', endpoint='index')
])

class Application(object):

    def __init__(self):
        self.endpoint_dict = {
        #'index':index
        #'test':test,
        }

    def route(self, rules, endpoint):
        def wrapper(func):
            url_map.add(Rule(rules, endpoint=endpoint))
            self.endpoint_dict[endpoint] = func
            return func
        return wrapper

    def __call__(self, environ, start_response):
        return self.application(environ, start_response)

    def application(self,environ, start_response):
        urls = url_map.bind_to_environ(environ)
        #url_map.add(Rule('/test/', endpoint='test'))
        environ = environ
        try:
            endpoint, args = urls.match()
        except HTTPException, e:
            return e(environ, start_response)

        return self.endpoint_dict[endpoint](start_response, **args)

app = Application()

@app.route('/', 'index')
def index(start_response, **args):
    start_response('200 OK', [('Content-Type','text/plain')])
    return "Welcome to Index!"

@app.route('/id/<int:id>', 'id')
def id(start_response, **args):
    start_response('200 OK', [('Content-Type','text/plain')])
    #return ["args: %s" % args["id"]]
    return "id is: %s" % args["id"]





run_simple('localhost', 8000, app, use_reloader = True)
