import socket
import threading
import time

class AmpelController:
	"""docstring for AmpelController"""
	def __init__(self):
		self.pins = {"red":24, "green":23}
		self.threads = {"red":None, "green":None}
		init_pin(self.pins["red"])
		init_pin(self.pins["green"])

	def __del__(self):
		for color in ["red","green"]:
			if self.threads[color]!=None:
				self.threads[color].stop()
			set_pin(self.pins[color],0)
			pin_off(self.pins[color])

	def blink(self,color,timeOn,timeOff):
		if self.threads[color]!=None:
			self.threads[color].stop()
		self.threads[color] = self.BlinkThread(self.pins[color],timeOn,timeOff)
		self.threads[color].start()
		return str.format("Blinking {} with {}/{}", color, timeOn, timeOff)

	def stop(self):
		for color in ["red","green"]:
			if self.threads[color]!=None:
				self.threads[color].stop()

	class BlinkThread (threading.Thread):
		"""docstring for myBlinkThread"""
		def __init__(self, pin,ontime,offtime):
			threading.Thread.__init__(self)
			self.pin = pin
			self.ontime = ontime
			self.offtime = offtime
			self.runFlag = ontime > 0

		def run(self):
			while self.runFlag:
				set_pin(self.pin,1)
				time.sleep(self.ontime)
				set_pin(self.pin,0)
				time.sleep(self.offtime)
		def stop(self):
			self.runFlag = False


def set_pin(pin,value):
	file('/sys/class/gpio/gpio'+str(pin)+'/value','w').write(str(value))

def init_pin(pin):
	file('/sys/class/gpio/export','w').write(str(pin))
	file('/sys/class/gpio/gpio'+str(pin)+'/direction','w').write('out')

def pin_off(pin):
	file('/sys/class/gpio/unexport','w').write(str(pin))