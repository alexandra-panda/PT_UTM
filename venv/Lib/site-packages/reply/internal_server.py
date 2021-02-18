from sys import version as python_version
from reply.server_template import RequestHandler
from cgi import parse_header, parse_multipart
import json

if python_version.startswith('3'):
    from urllib.parse import parse_qs
    from http.server import BaseHTTPRequestHandler, HTTPServer
else:
    from urlparse import parse_qs
    from BaseHTTPServer import BaseHTTPRequestHandler

class Server:


    def __init__(self, port, endpoints):
        self.__port = port
        url_map = {}
        for endpoint in endpoints:
            url_map[endpoint['url']] = endpoint['response']
        self.__endpoints = url_map

    def run(self):
        print('Starting server on 127.0.0.1:' + str(self.__port) + "")
        # Server settings
        server_address = ('127.0.0.1', int(self.__port))
        RequestHandler.get_url_map = self.__endpoints
        httpd = HTTPServer(server_address, RequestHandlerClass=RequestHandler)
        print('Running server...')
        httpd.serve_forever()