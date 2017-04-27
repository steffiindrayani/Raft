#!/usr/bin/python

class server:
	'identitas satu node'
	idserver = 0
	ip 		= 0
	port 	= 0
	load 	= 0
	isDead	= 0

	def __init__(self, ip, port, load):
		self.idserver =+1
		self.ip = ip
		self.port = port
		self.load = load

