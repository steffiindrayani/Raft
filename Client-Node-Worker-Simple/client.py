import requests
import simplejson

print ("----- CLIENT -----")

PORT_NODE = 9001 
NUMB = 20;
NUMB_JSON = simplejson.dumps({'JsonType':'CLIENT_REQUEST', 'PrimeRequest': + NUMB})

print (NUMB_JSON)
print ("Node Port : " + str(PORT_NODE))
print ("Prime Number Requested  : " + str(NUMB))

r = requests.post("http://localhost:" + str(PORT_NODE), data=NUMB_JSON)

print("---- RESPONSE : ---	")
#response
print(r.text) 