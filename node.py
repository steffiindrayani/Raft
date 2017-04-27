#!/usr/bin/python

class node:
   'identitas satu node'
   idnode = 0
   ip = 0
   port = 0
   status = "follower"
   timeout = 0


   def __init__(self, ip, port, status, timeout):
      node.idnode	+= 1
      node.ip 		= ip
      node.port 	= port
      node.status	= status
      node.timeout	= timeout

