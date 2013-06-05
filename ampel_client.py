#!/usr/bin/python2.7

import socket, time

s = socket.socket()
host = "192.168.178.96"
#host = "localhost"
port = 6000

s.connect((host, port))
print s.recv(1024)
print s.recv(1024)

try:
	while True:
		s.send("red 1")
		time.sleep(45)
		s.send("green 1")
		time.sleep(45)
		s.send("red 0")
		time.sleep(45)
		s.send("green 0")
except KeyboardInterrupt:
	print "Sigterm\n"
finally:
	s.close()