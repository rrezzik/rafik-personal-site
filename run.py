#!flask/bin/python

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from app import app

options.parse_command_line()
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(options.port)
IOLoop.instance().start()
#http_server = HTTPServer(WSGIContainer(app))
#http_server.listen(5000)
#IOLoop.instance().start()
#app.run(debug = True, host='0.0.0.0')
