#!/usr/bin/python
from datetime import datetime
from random import randint

class nodeInfo:
	idnode = 0
	ip = 0
	port = 0
	
	def __init__(self, ip, port):
		self.idnode	+= 1
		self.ip 		= ip
		self.port 	= port

class rivalC:
	idnode = 0
	numvote = 0

class node:
	nodeInfo = []
	status = "FOLLOWER"
	vote = 0
	timeout = 0
	startTime = 0
	timeoutServer = 0
	listneigh = []
	listserver = []
	listrival = []

	def __init__(self, nInfo):
		self.nodeInfo	= nInfo;
		self.timeout	= randint(2,5)
		self.startTime	= datetime.now()
	
	def resetTimeout(self):
		self.timeout = randint(2,5)
		self.startTime	= datetime.now()
		
	def isTimeOut(self):
		now = datetime.now()
		if ( (now - startTime).total_seconds() >= timeout):
			 return True
		return False
		
	def addNeigh(self, nInfo):
		self.listneigh.append(nInfo)
		
	def addServer(self, server):
		self.listServer.append(server)
	
	def candidacyRequest(self):
		if (self.isTimeOut == True):
			self.status = "CANDIDATE"
			'kirim ke semua klo u jd candidate'
			
	def recVoteCF(self):
		'terima reqvote dari candidate ke follower, follower bales response'
		

	def sendVoteCC(self):
		'kirim klo lu dapet vote ke candidate lain'
		
	
	def recVoteCC(self):
		'terima vote dari candidate lain'
		

	def setLeader(self):
		'kalo > jadi leader, kalo < jadi follower'
		
		
	def sendHeartbeat(self):
		'kirim heartbeat(load sm list) ke follower [post request] pake waktu bukan nunggu balesan'
		
	
	def recHeartbeat(self):
		'terima heartbeat dari follower [langsung response request]'
		
		
	def recServerLoad(self):
		'terima server load dari daemon'


