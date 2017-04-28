import psutil
import requests
import simplejson
import sys

SELF_PORT 		= int(sys.argv[1])
COUNT_OF_NODE 	= int(sys.argv[2])
LIST_OF_NODE 	= []
count 			= COUNT_OF_NODE
n 				= 3;

while count > 0:
	LIST_OF_NODE.append(int(sys.argv[n]))
	count	=- 1
	n 		=+ 1

class daemon():
	
	ip 			= 0
	port 		= 0
	load 		= 0
	
	def __init__(self):
		self.load = psutil.cpu_percent(interval = 1)
		self.ip	  = 'localhost'
		self.port = SELF_PORT

	def updateLoad(self):
		self.load = psutil.cpu_percent(interval = 1)
		
	def sendLoadtoNode(self):
		print ("-----DAEMON-----")
		LOAD_JSON = simplejson.dumps({'JsonType':'SERVER INFO', 'CPULoad': self.load, 'IP': self.ip, 'PORT': SELF_PORT})

		for node in LIST_OF_NODE:
		
			print (LOAD_JSON)
			print ("Node Port : " + str(node))
			print ("CPU Load  : " + str(self.load))

			r = requests.post("http://localhost:" + str(node), data=LOAD_JSON)

			print("---- RESPONSE : ---	")
			#response
			print(r.text) 

d = daemon()
while 1:
	d.sendLoadtoNode()
	d.updateLoad()

		
