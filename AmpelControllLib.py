#!/usr/bin/env python2.7

## Ampel-Controll lib

class AmpelControll:
	def __init__(self):
		pass

	# TODO: method to blink (params: color, on-duration, off-duration)
	def blink(self, color, dOn, dOff):
		pass

	# TODO: method for sequence of on-offs (params: color, interval, list of on/off)
	def blinkSequence(self, color, interval, sequence):
		if(set(sequence) == [0,1] or set(sequence) == [0] or set(sequence) == [1]):
			# do blinking stuff
			pass
		else:
			# malformed sequence
			pass

	# TODO: parse json with blink-settings
	def loadJSONSettings(self, jsonSettings):
		pass
		# TODO think of nice JSON structure for settings

'''

Ideas for JSON

Alternatively blinking with 1s Interval
{
	"interval":1,
	"red":[1,0],
	"green":[0,1],
	"iterations":0,
	"finalState":[0,0]
}

interval and (red|green) mandatory, rest optional

'''