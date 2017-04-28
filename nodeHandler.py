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

class NodeHandler(BaseHTTPRequestHandler):
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
			print("Message received. JsonType : " + JsonType)
			self.send_response(200)

			if JsonType == 'CLIENT_REQUEST': #Kalau Json Type yang diterima adalah dari Client.....        
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
				port = data['PORT']
				ip = data['IP']
				print("DAEMON IS SENDING CPU LOAD: " + str(CPULoad))
				if n.status == "LEADER":
					n.updateServerLoad(port, CPULoad)

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
					self.n.hasC = 1
				else:
					self.n.recVoteCF(ID_CANDIDATE)
			
			# elif JsonType == "VOTECC":

			elif JsonType == "HEARTBEAT":
				if self.voted == 1:
					self.voted = 0
				
				self.send_response(200)
				ServerPort = data['SERVER PORT']
				print ("Server with smallest load = " + str(ServerPort))
				self.n.resetTimeout()

				self.wfile.write(("Server Info Accepted").encode('utf-8'))
			
			elif JsonType == "CONFIG":
				global STARTOPERATING
				STARTOPERATING = 1
				print("StartOperating : " + str(STARTOPERATING))
				CountOfServer = int(data['CountOfServer'])
				CountOfNode = int(data['CountOfNode'])
				self.send_response(200)
				n.resetTimeout()

				i = 0
				while i < CountOfServer:
					s = "s" + str(i) 
					print("Server " + str(i) + ": " + str(data[s]))
					serv = server(ip, data[s], 0)
					n.addServer(serv)
					i += 1
				i = 0
				while i < CountOfNode:
					n = "n" + str(i)
					print("Node " + str(i) + ": " + str(data[n]))
					nInfo = nodeInfo(ip, data[n])
					n.addNeigh(nInfo)
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
			n = int(args[1])
			self.send_response(200)
			self.end_headers()
			url = "http://localhost:" + str(PORT_WORKER) + "/" + str(n)
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
	while 1:
		print(str(STARTOPERATING))
		if (STARTOPERATING):
			#Leader Election
			nH.n.candidacyRequest()

			if nH.n.status == "LEADER":
				nH.n.sendHeartbeat()
			else:
				print("Waiting for Heartbeat")
		else:
			print("Not Operating")
			time.sleep(1)
		
		time.sleep(0.5)


print('----- NODE -----')
print('SELF_PORT : ' + str(SELF_PORT))

server = HTTPServer(("", SELF_PORT), NodeHandler)
# thread1 = threading.Thread(target=server.serve_forever, args=())
_thread.start_new_thread(server.serve_forever, ())
main(NodeHandler)