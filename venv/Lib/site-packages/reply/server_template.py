from sys import version as python_version
from cgi import parse_header, parse_multipart
import json

if python_version.startswith('3'):
    from urllib.parse import parse_qs
    from http.server import BaseHTTPRequestHandler, HTTPServer
else:
    from urlparse import parse_qs
    from BaseHTTPServer import BaseHTTPRequestHandler

SERVER_PORT = 8081

class RequestHandler(BaseHTTPRequestHandler):

    """
    Class is auto-generated.
    Feel free to mess around!
    """

    get_url_map = {}

    @staticmethod
    def set_url_map(url_map):
        get_url_map = url_map


    def do_GET(self):
        # Send response status code
        self.log_request()
        if self.path in self.get_url_map:
            self.send_response(200)
            try:
                json.loads(self.get_url_map[self.path])
                self.send_header('Content-type', 'text/html')
            except json.decoder.JSONDecodeError:
                self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(self.get_url_map[self.path], "utf8"))
            return

        else:
            self.error_404()
        return


    def error_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("<h1>Error 404</h1>", "utf8"))
        return


    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                    self.rfile.read(length),
                    keep_blank_values=1)
        else:
            postvars = {}
        return postvars

    def do_POST(self):
        postvars = self.parse_POST()


def run():
    print('Starting server on 127.0.0.1:'+str(SERVER_PORT)+"")
    # Server settings
    server_address = ('127.0.0.1', SERVER_PORT)
    httpd = HTTPServer(server_address, RequestHandlerClass=RequestHandler)
    print('Running server...')
    httpd.serve_forever()
if __name__ == '__main__':
    run()