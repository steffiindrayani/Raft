#!/usr/bin/python
import requests
import simplejson
import sys

print ("----- CONFIG -----")

NUMBER_OF_NODE = int(sys.argv[1])
NUMBER_OF_SERVER = int(sys.argv[2])

FIRST_NODE = 13337
FIRST_SERVER = 9001

JSON = {'JsonType':'CONFIG', 'CountOfNode': + NUMBER_OF_NODE, 'CountOfServer': + NUMBER_OF_SERVER}
i = 0

while i < NUMBER_OF_NODE:
   JSON.update({'n' + str(i) : FIRST_NODE + i})
   i += 1

i = 0
while i < NUMBER_OF_SERVER:
   JSON.update({'s' + str(i) : FIRST_SERVER + i})
   i += 1

JSON_STRING = simplejson.dumps(JSON)

print (JSON_STRING)

# r = requests.post("http://localhost:" + str(PORT_NODE), data=NUMB_JSON)

# print("---- RESPONSE : --- ")
# response
# print(r.text) 
