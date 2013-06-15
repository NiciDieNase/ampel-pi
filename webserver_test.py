#!/usr/bin/env python2.7

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import time
import Ampel

controller=Ampel.AmpelController()

def main():
	try:
		server = HTTPServer(('localhost', 8888), MyHandler)
		print 'started httpserver...'
		server.serve_forever()
	except KeyboardInterrupt:
		print '^C received, shutting down server'
		controller.blink("red",0,0)
		controller.blink("green",0,0)
		server.socket.close()

class MyHandler(BaseHTTPRequestHandler):

#	def __init__(self):
#		super(self)
#		self.controller=Ampel.AmpelController()

	def do_GET(self):
		print "GET"
		print self.path
		self.send_response(200)
		self.send_header('Content-type', 'html')
		self.end_headers()
		self.wfile.write("<html> <head><title> Hello World </title> </head> <body>Hello World </body>")

	def do_PUT(self):
		print "----- SOMETHING WAS PUT!! ------"
		print self.headers
		length = int(self.headers['Content-Length'])
		content = self.rfile.read(length)
		result = json.loads(content)
		print result
		if("red" in result.keys() or "green" in result.keys()):
			self.send_response(200)
			self.handleJSON(result)
		else:
			self.send_response(400)

	def handleJSON(self,json):
		if ("red" in json.keys() and "green" in json.keys()):
			controller.blink("red",float(json["red"][0]),float(json["red"][1]))
			if "delay" in json.keys():
				time.sleep(float(json["delay"]))
			controller.blink("green",float(json["green"][0]),float(json["green"][1]))

		elif "red" in json.keys():
			controller.blink("red",float(json["red"][0]),float(json["red"][1]))

		elif "green" in json.keys():
			controller.blink("green",float(json["green"][0]),float(json["green"][1]))

if __name__ == '__main__':
	main()

