#! /usr/bin/python2

import urllib2
import gmpy
import time as Time
from threading import Thread

# This script provides the functonility of sending data to a server. Configuration (such as server address and such.) should be edited from the config file (server.config) and this scipt does not need to be edited. Import and use send_to_server() to send data. See docs.

# Shows debug messages
debug = True
cache_timer = 0
cache_start = 60 # time delay before sending cache

from time import sleep

def log(entry):
	f = open('collector.log', 'r')
	c_log = f.read()
	f.close()
	f = open('collector.log', 'w')
        f.write(c_log + str(entry) + "\n")
        f.close()

class Cache_time_keeper(Thread):
    global cache_timer
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global cache_timer
        if cache_timer !=0:
            cache_timer -=1
            sleep(1)
	
class Server:
	global debug, cache_timer, cache_start
	def __init__(self):
	        ct = Cache_time_keeper()
		# Get data from config.
		f = open("server.config")
		config = f.read()
		f.close()
		config_list = config.split("\n")
		self.cached_data = "lat,lng,stype,value,time;"
		for i in range(0, len(config_list)):
			if "PROTOCOL" in config_list[i]:
				self.protocol = config_list[i].split("=")[1]
			elif "DOMAIN" in config_list[i]:
				self.domain = config_list[i].split("=")[1]
			elif "PATH" in config_list[i]:
				self.path = config_list[i].split("=")[1]
			elif "METHOD" in config_list[i]:
				self.method = config_list[i].split("=")[1]
			elif "PASS" in config_list[i]:
				self.passcode = gmpy.mpz(config_list[i].split("=")[1])
				
	def log(self, entry):
		pre_log = ""
		try:
			f = open("server_comm.log","r")
			pre_log = f.read()
			f.close()
		except:
			pass
		f = open("server_comm.log","w")
		f.write(pre_log + entry + "\n")
		f.close()
	
	def send_to_server(self, data):
		global debug
		# Build the stage 2 url ready for sending data.
		# This is done first so as to decrease time between stage 1 and 2
		# Keys will timeout after 50 seconds by default.
		# Data is in csv string.
		url = self.protocol + self.domain + self.path + "?stage=2"
		url += "&dat=" + str(data)
		# get public key. 
		if debug:
			print "sending request to " + self.protocol + self.domain + self.path + "?stage=1"
		pubkeys = urllib2.urlopen(self.protocol + self.domain +self. path + "?stage=1").read()
		if debug:
			print "got public key: " + pubkeys
		n = gmpy.mpz(pubkeys.split(",")[0])
		e = gmpy.mpz(pubkeys.split(",")[1])
		c = ((self.passcode ** e)%n)
		if debug:
			print "encyrpted passcode as " + str(c)
		url += "&pass="+str(c)
		if debug:
			print "Sending " + url
		response = urllib2.urlopen(url).read()
		if debug:
			print "got response: "+response
		return response
	
	def submit_data(self, lat, lng, stype, value, time, cache=False, data=""):
        	global cache_timer, cache_start
	        if data == "": #Regular submit
			if cache == False:
				dat = "lat,lng,stype,value,time;"
				dat += str(lat)+","+str(lng)+","+str(stype)+","+str(value)+","+str(time)+";"
				print 'going to send to serveer def'
				r = self.send_to_server(dat)
			if cache:
				self.cached_data += str(lat)+","+str(lng)+","+str(stype)+","+str(value)+","+str(time)+";"
				r = "success"
				if cache_timer == 0:
					cache_timer = cache_start
		else: # Submit from cache timer
			r = send_to_server(data)
		if not "success" in r:
                	if r == "authenication failure":
                    		print "ALERT: Passcode rejected by server."
                    		log("Passcode rejected. " + str(time.time()))
                	if r == "timeout":
                    		log("Timeout." + str(time.time()))
                else:
                    print "ERROR:" + str(r)
                    log(str(r) + str(Time.time()))



