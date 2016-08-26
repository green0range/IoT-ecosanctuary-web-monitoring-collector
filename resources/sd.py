#! /usr/bin/python

import math
import serial
import time

file = time.time()

def get_passcodes():
	#try:
		f = open(".receiverpass")
		codes = f.read().split("\n")
		print codes
		passes = []
		print "l:"+str(len(codes))
		for i in range(0, len(codes)-1):
			print i
			if not list(codes[i])[0] == "#":
				passes.append(int(codes[i]))
		return passes
	#except:
	#print "ERROR: No .receiverpass file found."
	
logdata = ""
auto_saves = 1
def log(entry):
	global logdata, autosaves, file 
	logdata  += str(entry) +"\n"
	if len(logdata)>100*auto_saves: # auto save
		f = open(file + ".log", "w")
		f.write(logdata)
		f.close()
		
def display_input(port="/dev/ttyAMA0", baud=2400):
	ser = serial.Serial(port, baud, timeout=2)
	codes = get_passcodes()
	while True:
		data = ser.readline()
		print data
		log(data)
		if "SetRe" in data:
			time.sleep(1)
			picaxe_config = "conf:\x0A\x0AM\x00" 
			#print picaxe_config
			ser.write(picaxe_config)
			print "sent config..."
		"""
		data_array = list(data)
		for i in range(0, len(data_array)):
			if ord(data_array[i]) == 254:
				data_array[i] = "\n" # 254 is used instead of 10, so that it doesn't end the line during serial transmit, this turns it back.
		try:
			checksum = ord(data_array.pop(len(data_array-1)))
		except:
			checksum = 500
		check = 0
		for j in range(0, len(data_array)):
            		check += ord(data_array[j])
            	for i in range(0, len(codes)):
            		check += int(codes[i])
        	check = (check/((len(data_array) + len(codes))))
		check = int(math.floor(check))
		#print "CHECK:	" + str(check) + "CHECKSUM:	" + str(checksum)
        	for i in range(0, len(data_array)):
        		data_array[i] = ord(data_array[i])
        	if check == checksum:
        		print "Received data: " + str(data_array)
        		# Add processing functions here
        	else:
        		if checksum != 500:
        			print "Data with error: " + str(data_array)
        	"""	
        		
display_input()
			
