#!/usr/bin/python

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

	
"This would create first object of Employee class"
emp1 = client("1", "1", 1)
print "ip %d" % emp1.numberrequested
