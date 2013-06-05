#!/usr/bin/env python2.7

import socket

red = 24
green = 23

def main():
	init_pin(green)
	init_pin(red)
	s = socket.socket()
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
					msg = c.recv(16);
					if len(msg) <= 2:
						break
					msg = msg.split(" ")
					msg[1] = msg[1][0]
					print msg
					if msg[0] == "green":
						if msg[1] == '0':
							c.send("Turning of green\n")
							set_pin(green,0)
						elif msg[1] == '1':
							c.send("Turning on green\n")
							set_pin(green,1)
						else:
							c.send("error\n")
					elif msg[0] == "red":
						if msg[1] == '0':
							c.send("Turning of red\n")
							set_pin(red,0)
						elif msg[1] == '1':
							c.send("Turning on red\n")
							set_pin(red,1)
						else:
							c.send("error\n")
					else:
						c.send("error\n")
			except socket.error:
				print "Connection reset"
			finally:
				c.close()
	except KeyboardInterrupt:
		print "Sigterm\n"
	finally:
		print "kthxbye\n"
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

if __name__ == "__main__":
	main()
