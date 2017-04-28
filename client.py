#!/usr/bin/python
import requests
import simplejson

class client:
   'identitas satu node'
   ip = 0
   port = 0
   numberrequested = 0


   def __init__(self):
      localhost 	= '120.0.0.1'
      client.ip 	= localhost
      client.port 	= '4040'
      client.numberrequested	= 0 

   def __init__(self, ip, port, number):
      client.ip 	= ip
      client.port 	= port
      client.numberrequested	= number

print ("----- CLIENT -----")

PORT_NODE = sys.argv[1]
NUMB = sys.argv[2]
NUMB_JSON = simplejson.dumps({'JsonType':'CLIENT_REQUEST', 'PrimeRequest': + NUMB})

print (NUMB_JSON)
print ("Node Port : " + str(PORT_NODE))
print ("Prime Number Requested  : " + str(NUMB))

r = requests.post("http://localhost:" + str(PORT_NODE), data=NUMB_JSON)

print("---- RESPONSE : --- ")
#response
print(r.text) 