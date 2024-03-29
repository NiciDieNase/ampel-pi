#!/usr/bin/env python2.7

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import json
import threading
import time
import Ampel

controller=Ampel.AmpelController()

def main():
	try:
		controller.set_color("red",1)
		controller.set_color("green",1)

		controller.blink("red",1.0,1.0)
		time.sleep(1.0)
		controller.blink("green",1.0,1.0)

		server = HTTPServer(('0.0.0.0', 80), MyHandler)
		print 'started httpserver...'
		server.serve_forever()
	except KeyboardInterrupt:
		print '^C received, shutting down server'
		controller.stop("red")
		controller.stop("green")
		server.socket.close()

class MyHandler(BaseHTTPRequestHandler):

#	def __init__(self):
#		super(self)
#		self.blacklist=[]
#		self.controller=Ampel.AmpelController()
		

	def do_GET(self):
#		print "GET"
#		print self.path
		if self.path=="/0":
			controller.set_color("red",0)
			controller.set_color("green",0)
		elif self.path=="/1":
			controller.set_color("red",0)
			controller.set_color("green",1)
		elif self.path=="/2":
			controller.set_color("red",1)
			controller.set_color("green",0)
		elif self.path=="/3":
			controller.set_color("red",1)
			controller.set_color("green",1)
		self.send_response(200)
		self.send_header('Content-type', 'html')
		self.end_headers()
		self.wfile.write(open(os.path.join(os.path.dirname(__file__), 'info.html')).read())

	def do_PUT(self):
		self.handleData()

	def do_POST(self):
		self.handleData()


	def handleData(self):
		blacklist=[]
		if not self.client_address[0] in blacklist:
#			print self.path
			if self.path == "/":
				length = int(self.headers['Content-Length'])
				content = self.rfile.read(length)
				result = json.loads(content)
				#print json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
				print result
				if("red" in result.keys() or "green" in result.keys()):
					self.send_response(200)
					self.handleJSON(result)
				else:
					self.send_response(400)
			else:
				if self.path=="/0":
					controller.set_color("red",0)
					controller.set_color("green",0)
				elif self.path=="/1":
					controller.set_color("red",0)
					controller.set_color("green",1)
				elif self.path=="/2":
					controller.set_color("red",1)
					controller.set_color("green",0)
				elif self.path=="/3":
					controller.set_color("red",1)
					controller.set_color("green",1)
				else:
					self.send_response(400)
		else:
			print "Blocked request from ", self.client_address[0]
			self.send_response(402)

	def handleJSON(self,json):
		#print json
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

