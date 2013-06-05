#!/usr/bin/python2.7

import socket, time

s = socket.socket()
host = "192.168.178.96"
#host = "localhost"
port = 6000

s.connect((host, port))
print s.recv(1024)
print s.recv(1024)

time.sleep(1)
s.send("green 1")
time.sleep(1)
s.send("red 1")
time.sleep(1)


s.close()