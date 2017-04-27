#!/usr/bin/python
from datetime import datetime
from random import randint

class nodeInfo:
	idnode = 0
	ip = 0
	port = 0
	status = "FOLLOWER"
	
	def __init__(self, ip, port, status):
      self.idnode	+= 1
      self.ip 		= ip
      self.port 	= port
      self.status	= status
      
    def setStatus(self, status):
      self.status	= status
		

class node:
	timeout = 0
	startTime = 0
	listneigh = []
	listserver = []

	def __init__(self):
		self.timeout	= randint(2,5)
		self.startTime	= datetime.now()
	
	def resetTimeout(self):
		self.timeout = randint(2,5)
		
	def isTimeOut(self):
		currNow = datetime.now()
		if (currNow - startTime >= timeout):
			 return True
		return False
		
	def addNeigh(self, nInfo):
		self.listneigh.append(nInfo)
		
	def addServer(self, server):
		self.listServer.append(server)
	
	
