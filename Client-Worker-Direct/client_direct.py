import requests
import simplejson

print ("----- CLIENT DIRECT TO WORKER -----")

PORT_WORKER = 13337 
NUMB = 20; #prime number requested
# NUMB_JSON = simplejson.dumps({'num': + NUMB})

# print (NUMB_JSON)
# print ("Node Port : " + str(PORT_NODE))
# print ("Prime Number Requested  : " + str(NUMB))

r = requests.get("http://localhost:" + str(PORT_WORKER) + '/' + str(NUMB))

# response
print(r.text) 