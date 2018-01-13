# -*- coding: UTF-8 -*-
#smartframe.py


class Application(object):

    def __init__(self):
        pass
        self.routes = {}
    def route(self, path=None):
        def wrapper(func):
            self.routes[path] = func
            return func
        return wrapper

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']
        if path in self.routes:
            status = '200 OK'
            response_headers = [('Content-Type','text/html')]
            start_response(status, response_headers)
            return self.routes[path]()
            #return routes[path]()
        else:
            status = '404 Not Found'
            response_headers = [('Content-Type','text/html')]
            start_response(status, response_headers)
            return "<h1>homepage</h1><p>{}</p>".format(environ)
