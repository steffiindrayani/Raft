#!/usr/bin/python
from datetime import datetime
from random import randint
import requests
import simplejson

ipG = 'localhost'

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
	majorVote = 0

	def __init__(self, nInfo):
		self.nodeInfo	= nInfo;
	
	def resetTimeout(self):
		self.timeout = 4
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
		# print("START UPDATE")
		for aaa in self.listserver:
			# print("Server di UPDATE: " + str(aaa.port))
			if aaa.port == port:
				self.listserver.remove(aaa)
		serv = server(ipG, port, load)
		self.addServer(serv)

	def addRival(self, rivalC):
		self.listrival.append(rivalC)
	
	def candidacyRequest(self):
		if (self.isTimeOut() == True):
			self.status = "CANDIDATE"
			self.vote += 1
			print ("-----CANDIDACY REQUEST-----")
			LOAD_JSON = simplejson.dumps({'JsonType':'CANDIDACY REQUEST', 'IDNODE': + self.nodeInfo.idnode, 'PORT': + self.nodeInfo.port})

			for node in self.listneigh:
				print ("Destination : " + str(node.port))
				print ("My Port : " + str(self.nodeInfo.port))

				print("---- CANREQ RESPONSE : ----")
				try:
					r = requests.post("http://localhost:" + str(node.port), data=LOAD_JSON)
					rVote = int(r.text)
					self.vote += rVote
					if rVote == 1:
						self.sendVoteCC()
				except:
					print("Connection Lost to Port: " + str(node.port))

				print()
				self.resetTimeout()

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

			print("---- CANDIDATE RESPONSE : ----")
			try:
				r = requests.post("http://localhost:" + str(node.port), data=LOAD_JSON)
			except:
				print("Connection Lost to Port: " + str(node.port))
	
	def recVoteCC(self, idR):
		idCandidate = idR
		for rival in self.listrival:
			if rival.idnode == idCandidate:
				rival.numvote += 1

	def isRestartElection(self):
		idR = 0;
		for rival in self.listrival:
			if self.vote == rival.numvote:
				idR = rival.idnode
		return idR != 0

	def setLeader(self):
		if self.status == "CANDIDATE":
			mxVote = self.majorVote
			print("My Vote: " + str(self.vote))
			print("Winning Vote: " + str(mxVote))
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
		print ("[HEARTBEAT]")
		servPort = self.getSmallestLoad()
		LOAD_JSON = simplejson.dumps({'JsonType':'HEARTBEAT', 'SERVER PORT': + servPort})
		self.resetTimeout()
		print ("Sending heartbeat")
		print ("My Port : " + str(self.nodeInfo.port) + "\n")

		for node in self.listneigh:
			print ("Destination : " + str(node.port))
			print ("Server Port : " + str(servPort))

			print("Heartbeat Response :")
			try:
				r = requests.post("http://localhost:" + str(node.port), data=LOAD_JSON)
			except:
				print("Connection Lost to Port: " + str(node.port))
			print("----")
			# print(r.text)
		
