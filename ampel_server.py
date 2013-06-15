#!/usr/bin/env python2.7

import socket
import threading
import time

red = 24
green = 23

def main():
	init_pin(green)
	init_pin(red)
	s = socket.socket()
	threadRed = None
	threadGreen = None
	try:
#		host = socket.gethostname()
		host = "0.0.0.0"
		port = 6000
		s.bind((host, port))
		s.listen(5)

		while True:
			c, addr = s.accept()
			try:
				print 'Connection opend', addr
				c.send("ohai\n")
				c.send("Commands are '[red|green] [0|1]'\n")
				while True: 
					msg = c.recv(32);
					if len(msg) <= 2:
						break
					msg=msg[0:-2]
					msg = msg.split(" ")
#					msg[1] = msg[1][0]
					print msg
					if msg[0] == "green":
						if threadGreen != None:
							threadGreen.stop()
						if msg[1] != '0':
							threadGreen = myBlinkThread(green,float(msg[1]),float(msg[2]))
							threadGreen.start()
					elif msg[0] == "red":
						if threadRed != None:
							threadRed.stop()
						if msg[1] != '0':
							threadRed = myBlinkThread(red,float(msg[1]),float(msg[2]))
							threadRed.start()
					elif msg[0] == "both":
						if threadRed != None:
							threadRed.stop()
						if threadGreen != None:
							threadGreen.stop()
						if msg[1] != '0':
							threadRed = myBlinkThread(red,float(msg[1]),float(msg[2]))
							threadGreen = myBlinkThread(green,float(msg[3]),float(msg[4]))
							threadRed.start()
							if len(msg) > 5:
								time.sleep(float(msg[5]))
							threadGreen.start()
					else:
						c.send("error\n")
			except socket.error:
				print "Connection reset"
			except KeyboardInterrupt:
				c.close()
				if threadGreen != None:
					threadGreen.stop()
				if threadRed != None:
					threadRed.stop()
	except KeyboardInterrupt:
		print "Sigterm\n"
	except:
		print "error\n"
	finally:
		print "kthxbye\n"
		if threadGreen != None:
			threadGreen.stop()
		if threadRed != None:
			threadRed.stop()
		pin_off(red)
		pin_off(green)
#		s.shutdown(socket.SHUT_RDWR)
		s.close()

def set_pin(pin,value):
	file('/sys/class/gpio/gpio'+str(pin)+'/value','w').write(str(value))

def init_pin(pin):
	file('/sys/class/gpio/export','w').write(str(pin))
	file('/sys/class/gpio/gpio'+str(pin)+'/direction','w').write('out')

def pin_off(pin):
	file('/sys/class/gpio/unexport','w').write(str(pin))

class myBlinkThread (threading.Thread):
	"""docstring for myBlinkThread"""
	def __init__(self, pin,ontime,offtime):
		threading.Thread.__init__(self)
		self.pin = pin
		self.ontime = ontime
		self.offtime = offtime
		self.runFlag = True
	def run(self):
		while self.runFlag:
			set_pin(self.pin,1)
			time.sleep(self.ontime)
			set_pin(self.pin,0)
			time.sleep(self.offtime)
	def stop(self):
		self.runFlag = False


if __name__ == "__main__":
	main()