#Copyright (c) 2012, Carnegie Mellon University.
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions
#are met:
#1. Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#2. Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#3. Neither the name of the University nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.

import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

from cmurrd import *

class TestRequest:
    def __init__(self):
        self.GET = {}

#Handle HTTP requests for data only.
class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		prefix = "/q?"
		if self.path.startswith(prefix):
			#split the query string if it starts with the prefix
			qs = self.path[len(prefix):]
			qsparts = qs.split("&")
			request = TestRequest()
			for qsp in qsparts:
				parts = qsp.split("=")
				request.GET[parts[0]] = "=".join(parts[1:])
			res = DATA.fetch(request)
		else:
			res = "Unknown path:" + self.path

		self.send_response(200)
		self.end_headers()
		self.wfile.write(res)

HandlerClass = Handler #SimpleHTTPRequestHandler
ServerClass = BaseHTTPServer.HTTPServer
Protocol = "HTTP/1.0"
HandlerClass.protocol_version = Protocol

if __name__ == '__main__':
	httpd = ServerClass(("0.0.0.0",8000), HandlerClass)
	#Try me with 
	#http://<ip>:8000
	#/q?start=2011/12/11-8:30:00&end=2012/01/20-8:30:00&m=sum:median{host=LocalMachine}
	print "Serving on ", httpd.socket.getsockname()

	DATA = get_cmu()
	httpd.serve_forever()