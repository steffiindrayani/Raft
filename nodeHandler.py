#!/usr/bin/env python
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

class NodeHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            args = self.path.split('/')
            if len(args) != 2:
                raise Exception()
            n = int(args[1])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(self.calc(n)).encode('utf-8'))
        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)

server = HTTPServer(("", PORT), NodeHandler)
server.serve_forever()
