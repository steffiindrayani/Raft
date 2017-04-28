#!/usr/bin/python
from datetime import datetime
from random import randint
import requests
import simplejson

class nodeInfo:
	idnode = 0
	ip = 0
	port = 0
	
	def __init__(self, ip, port):
		self.idnode	+= 1
		self.ip 	= ip
		self.port 	= port

class rivalC:
	idnode = 0
	numvote = 0

	def __init__(self, idnode, numvote):
		self.idnode = idnode
		self.numvote = numvote

class server:
	ip = 0
	port = 0
	load = 0

	def __init__(self, ip, port, load):
		self.ip = ip
		self.port = port
		self.load = load

class node:
	nodeInfo = nodeInfo(0, 0)
	status = "FOLLOWER"
	vote = 0
	timeout = 0
	startTime = 0
	timeoutServer = 0
	listneigh = []
	listserver = []
	listrival = []
	voted = 0
	hasC = 0

	def __init__(self, nInfo):
		self.nodeInfo	= nInfo;
	
	def resetTimeout(self):
		self.timeout = randint(3,5)
		self.startTime	= datetime.now()
		
	def isTimeOut(self):
		now = datetime.now()
		if ( (now - self.startTime).total_seconds() >= self.timeout):
			 return True
		return False
		
	def addNeigh(self, nInfo):
		self.listneigh.append(nInfo)
		
	def addServer(self, server):
		self.listserver.append(server)

	def updateServerLoad(self, port, load):
		for index in range(len(self.listserver)):
			if self.listserver[index].port == port:
				self.listserver[index].load = load

	def addRival(self, rivalC):
		self.listrival.append(rivalC)
	
	def candidacyRequest(self):
		if (self.isTimeOut() == True):
			self.status = "CANDIDATE"
			print ("-----CANDIDACY REQUEST-----")
			LOAD_JSON = simplejson.dumps({'JsonType':'CANDIDACY REQUEST', 'IDNODE': + self.nodeInfo.idnode, 'PORT': + self.nodeInfo.port})
			
			for node in self.listneigh:
				print ("Sending heartbeat")
				print ("Destination : " + str(node.port))
				print ("My Port : " + str(self.nodeInfo.port))

				r = requests.post("http://localhost:" + str(node.port), data=LOAD_JSON)

				print("---- CANREQ RESPONSE : ----")
				# print(r.text)
		self.setLeader()

	def recVoteCF(self, idC):
		idCandidate = idC
		if self.status == "CANDIDATE":
			cand = rivalC(idCandidate, 0)
			self.addRival(rivalC)

	def sendVoteCC(self):
		print ("-----I GOT A VOTE-----")
		LOAD_JSON = simplejson.dumps({'JsonType':'VOTECC', 'IDNODE': + self.nodeInfo.idnode, 'PORT': + self.nodeInfo.port})
		
		for node in self.listrival:
			print ("Rival Port : " + str(node.port))
			print ("My Port : " + str(self.nodeInfo.port))

			r = requests.post("http://localhost:" + str(node.port), data=LOAD_JSON)

			print("---- CANDIDATE RESPONSE : ----")
			rVote = int(r.text)
			# print(r.text)
			self.vote += rVote
	
	def recVoteCC(self, id):
		idCandidate = id
		for rival in self.listrival:
			if rival.idnode == idCandidate:
				rival.numvote += 1

	def maxVote(self):
		mxVote = 0;
		for vote in self.listrival:
			if mxVote < vote.numvote:
				mxVote = vote.numvote
		return mxVote

	def setLeader(self):
		if self.status == "CANDIDATE":
			mxVote = self.maxVote()
			if self.vote < mxVote:
				self.status = "FOLLOWER"
			else:
				self.status = "LEADER"
			self.vote = 0
			self.listrival = []
		
	def getSmallestLoad(self):
		minLoad = 999
		minPort = 0
		for server in self.listserver:
			if minLoad > server.load:
				minLoad = server.load
				minPort = server.port
		return minPort

	def sendHeartbeat(self):
		print ("-----HEARTBEAT-----")
		servPort = self.getSmallestLoad()
		LOAD_JSON = simplejson.dumps({'JsonType':'HEARTBEAT', 'SERVER PORT': + servPort})
		self.resetTimeout()
		for node in self.listneigh:
			print ("Sending heartbeat")
			print ("Destination : " + str(node.port))
			print ("My Port : " + str(self.nodeInfo.port))

			r = requests.post("http://localhost:" + str(node.port), data=LOAD_JSON)

			print("---- HEARTBEAT RESPONSE : ----")
			# print(r.text)
		
