#coding: utf-8
#server.py

from wsgiref.simple_server import make_server
from smartframe import *

app = Application()

@app.route('/hehe/')
def hehe():
    return "hehe"

httpd = make_server('', 8001, app)
print "Server start on port 8001"

httpd.serve_forever()
