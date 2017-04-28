import psutil
import requests
import simplejson

PORT_NODE = 9001

class daemon():
	
	ip = 0
	port = 0
	load = 0
	
	def __init__(self):
		self.load = psutil.cpu_percent(interval = 1)
	
	def updateLoad(self):
		self.load = psutil.cpu_percent(interval = 1)
		
	def sendLoadtoNode(self, port, load):
		print ("-----DAEMON-----")
		LOAD_JSON = simplejson.dumps({'JsonType':'SERVER INFO', 'PORT': + port, 'CPULoad': + load})
		
		print (LOAD_JSON)
		print ("Node Port : " + str(PORT_NODE))
		print ("CPU Load  : " + str(load))

		r = requests.post("http://localhost:" + str(PORT_NODE), data=LOAD_JSON)

		print("---- RESPONSE : ---	")
		#response
		print(r.text) 

d = daemon()
while 1:
	d.sendLoadtoNode(d.load)
	d.updateLoad()

		
