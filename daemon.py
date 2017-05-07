from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

import _thread
import psutil
import requests
import simplejson
import sys
import time

SELF_PORT 		= int(sys.argv[1])
COUNT_OF_NODE 	= int(sys.argv[2])
LIST_OF_NODE 	= []
count 			= COUNT_OF_NODE
print(COUNT_OF_NODE)

for i in range(1, count + 1): 
	print(i)
	LIST_OF_NODE.append(int(sys.argv[i + 2]))
	print(int(sys.argv[i + 2]))

class WorkerHandler(BaseHTTPRequestHandler):
    def prime(self, n):
        i = 2
        while i * i <= n:
            if n % i == 0:
                return False
            i += 1
        return True

    def calc(self, n):
        p = 1
        while n > 0:
            p += 1
            if self.prime(p):
                n -= 1
        return p

    def do_GET(self):
        try:
            args = self.path.split('/')
            if len(args) != 2:
                raise Exception()
            n = int(args[1])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(self.calc(n)).encode('utf-8'))
        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)

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

			try:
				r = requests.post("http://localhost:" + str(node), data=LOAD_JSON)
			except:
				print("Connection Lost to Port: " + str(node))

			print("---- RESPONSE : ---	")
			#response
			print(r.text) 


server = HTTPServer(("", SELF_PORT), WorkerHandler)
# thread1 = threading.Thread(target=server.serve_forever, args=())
_thread.start_new_thread(server.serve_forever, ())



d = daemon()
while 1:
	d.sendLoadtoNode()
	d.updateLoad()
	time.sleep(1)

		
