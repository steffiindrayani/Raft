#!/usr/bin/python

from node import node
from server import server
from datetime import datetime

class loadbalancer():
	
	listnode = []
	listserver = []
	leadertimeout = 10
	servertimeout = 10
	startwaitleader = 0
	startwaittimeout = 0
	

	def __init__(self, numberOfNode, numberOfServer):
		for i in range (1, numberOfNode):
			loadbalancer.listnode.append(node("120.0.0.1", "4040", "follower", "5"))
		for i in range (1, numberOfServer):
			loadbalancer.listserver.append(server("120.0.0.1", "4040", "5"))			

	def isLeaderTimeOut(self):
		currtime = datetime.now()
		if (currtime - startwaitleader > 0) return True else return False
		
	
