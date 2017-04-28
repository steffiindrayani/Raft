#!/usr/bin/python
from datetime import datetime
from random import randint

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

	def addRival(self, rivalC):
		self.listrival.append(rivalC)
	
	def candidacyRequest(self):
		if (self.isTimeOut == True):
			self.status = "CANDIDATE"
			'kirim ke semua klo u jd candidate'

	def recVoteCF(self):
		'terima reqvote dari candidate ke follower, follower bales response, candidate append list'
		idCandidate = 0
		if self.status == "FOLLOWER":
			#response
		else if self.status == "CANDIDATE"
			cand = rivalC(idCandidate, 0)
			addRival(rivalC)

	def sendVoteCC(self):
		'kirim klo lu dapet vote ke candidate lain'
		
	
	def recVoteCC(self):
		'terima vote dari candidate lain'
		idCandidate = 0
		for rival in listrival:
			if rival.idnode == idCandidate:
				rival.numvote += 1

	def maxVote(self):
		mxVote = 0;
		for vote in listrival:
			if mxVote < vote.numvote:
				mxVote = vote.numvote
		return mxVote

	def setLeader(self):
		if self.status == "CANDIDATE":
			mxVote = maxVote()
			if self.vote < mxVote:
				self.status = "FOLLOWER"
			else
				self.status = "LEADER"
			vote = 0
			listrival = []
		
	def sendHeartbeat(self):
		'kirim heartbeat(load sm list) ke follower [post request] pake waktu bukan nunggu balesan'
		print ("-----HEARTBEAT-----")
		LOAD_JSON = simplejson.dumps({'JsonType':'SERVER INFO', 'PORT': + port, 'CPULoad': + load})
		
		print (LOAD_JSON)
		print ("Node Port : " + str(PORT_NODE))
		print ("CPU Load  : " + str(load))

		r = requests.post("http://localhost:" + str(PORT_NODE), data=LOAD_JSON)

		print("---- RESPONSE : ---	")
		#response
		print(r.text) 
	
	def recHeartbeat(self):
		'terima heartbeat dari follower [langsung response request]'
		
		
	def recServerLoad(self):
		'terima server load dari daemon'


