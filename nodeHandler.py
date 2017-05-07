#!/usr/bin/env python
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import requests
import simplejson
import sys
from node import node
from node import nodeInfo
from node import server
from node import rivalC
import time
import threading
import _thread

SELF_PORT = int(sys.argv[1])
ip = 'localhost'
STARTOPERATING = 0
PORT_WORKER = 13337 # INI YANG DIAMBIL

class NodeHandler(BaseHTTPRequestHandler	):
	nInfo = nodeInfo(ip, SELF_PORT)
	n = node(nInfo)

	def do_POST(self):
		try:
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.data_string = self.rfile.read(int(self.headers['Content-Length']))
			self.end_headers()
			data = simplejson.loads((self.data_string))
			JsonType = data['JsonType']
			self.send_response(200)

			if JsonType == 'CLIENT_REQUEST':
				PrimeRequest = data['PrimeRequest']
				print("CLIENT IS REQUESTING PRIME NUMBER: " + str(PrimeRequest))
				url = "http://localhost:" + str(PORT_WORKER) + "/" + str(PrimeRequest)
				r = requests.get(url)
				if r.status_code == 200:
					self.send_response(200)
					answer = r.text
					print(r.text)
					self.wfile.write(str(r.text).encode('utf-8'))                
				else:
					self.send_response(500)
					self.wfile.write(str(-1).encode('utf-8'))
			
			elif JsonType == 'SERVER INFO':
				CPULoad = data['CPULoad']
				port = int(data['PORT'])
				if self.n.status == "LEADER":
					print("DAEMON IS SENDING CPU LOAD: " + str(CPULoad) + " on PORT : " + str(port))
					self.n.updateServerLoad(port, CPULoad)

			elif JsonType == 'CANDIDACY REQUEST':
				ID_CANDIDATE = data['IDNODE']
				PORT_CANDIDATE = data['PORT']
				print ("NODE " + str(PORT_CANDIDATE) + " ASK FOR VOTE")
				
				if self.n.status == 'FOLLOWER':
					if self.n.voted == 0:
						self.wfile.write(("1").encode('utf-8'))
						self.n.voted = 1
						self.n.resetTimeout()
					else:
						self.wfile.write(("0").encode('utf-8'))
				else:
					self.n.recVoteCF(ID_CANDIDATE)
			
			elif JsonType == "VOTECC":
				if self.n.status == 'CANDIDATE':
					ID_RIVAL = data['IDNODE']
					PORT_RIVAL = data['PORT']
					print ("RIVAL NODE " + str(PORT_RIVAL) + " GOT A VOTE")
				
					recVoteCC(ID_RIVAL)

			elif JsonType == "HEARTBEAT":
				if self.n.voted == 1:
					self.n.voted = 0
				
				self.send_response(200)
				ServerPort = data['SERVER PORT']
				self.n.resetTimeout()

				self.wfile.write(("Server Info Accepted").encode('utf-8'))
			
			elif JsonType == "CONFIG":
				global STARTOPERATING
				STARTOPERATING = 1
				print("StartOperating : " + str(STARTOPERATING))
				CountOfServer = int(data['CountOfServer'])
				CountOfNode = int(data['CountOfNode'])
				self.send_response(200)
				self.n.resetTimeout()
				self.n.majorVote = (CountOfNode + 1) / 2
				i = 0
				while i < CountOfServer:
					s = "s" + str(i) 
					print("Server " + str(i) + ": " + str(data[s]))
					serv = server(ip, data[s], 0)
					self.n.addServer(serv)
					i += 1

				i = 0
				while i < CountOfNode:
					nx = "n" + str(i)
					print("Node " + str(i) + ": " + str(data[nx]))
					nInfo = nodeInfo(ip, data[nx])
					self.n.addNeigh(nInfo)
					i += 1

		except Exception as ex:
			self.send_response(500)
			self.end_headers()
			print(ex)

	def do_GET(self):
		try:
			args = self.path.split('/')
			if len(args) != 2:
				raise Exception()
			prime_number_requested = int(args[1])
			self.send_response(200)
			self.end_headers()
			PORT_WORKER = self.n.getSmallestLoad()
			url = "http://localhost:" + str(PORT_WORKER) + "/" + str(prime_number_requested)
			r = requests.get(url)
			answer = r.text
			print(answer)
			self.wfile.write("[Response] ".encode('utf-8'))                
			self.wfile.write("Prime Number: ".encode('utf-8'))                
			self.wfile.write(str(r.text).encode('utf-8'))                
			self.send_response(200)

		except Exception as ex:
			self.send_response(500)
			self.end_headers()
			print(ex)

def main(NodeHandler):
	nH = NodeHandler
	stop = False
	while stop == False:
		if (STARTOPERATING):
			#Leader Election
			nH.n.candidacyRequest()
			if nH.n.isRestartElection():
				print("\nLEADER NOT SELECTED. RESTARTING ELECTION.\n")
			else:
				if nH.n.status == "LEADER":
					nH.n.sendHeartbeat()
					time.sleep(1)
				elif nH.n.status == "FOLLOWER":
					print("[FOLLOWER] Waiting for Heartbeat | " + str(SELF_PORT))
				else:
					print("I'm a CANDIDATE")
		else:
			print("Not Operating")
			time.sleep(1)
		
		time.sleep(1)


print('----- NODE -----')
print('SELF_PORT : ' + str(SELF_PORT))

server = HTTPServer(("", SELF_PORT), NodeHandler)
_thread.start_new_thread(server.serve_forever, ())
main(NodeHandler)