#!/usr/bin/python

class server:
   'identitas satu node'
   idserver = 0
   ip 		= 0
   port 	= 0
   load 	= 0


   def __init__(self, ip, port, load):
	   server.idserver =+1
	   server.ip = ip
	   server.port = port
	   server.load = load

	
