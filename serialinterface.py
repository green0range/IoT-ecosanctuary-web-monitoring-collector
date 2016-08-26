#! /usr/bin/python

import math
import serial
import time

class Connection:
	def __init__(self):
		# Setup port and baudrate
		self.port="/dev/ttyAMA0"
		self.baud=2400
		self.trans_method = ord('M') # or P
		self.handshake = ord("\x00")
		#open serial port
		self.ser = serial.Serial(self.port, self.baud, timeout=2)
		# Get codes on start up
		try:
			f = open(".receiverpass")
			codes = f.read().split("\n")
			self.codes = []
			for i in range(0, len(codes)):
				if not list(codes[i])[0] == '#':
					self.codes.append(int(codes[i]))
		except:
			pass
	def get_input(self):
		self.ser = serial.Serial(self.port, self.baud, timeout=2)
		data = "" # clear data to avoid loops
		data = self.ser.readline()
		print data
		if ":01" in data: # completely igorng, the communication is 2 way domn one line so anything adressed to the picaxe is a loopback.
			print "got feedback"
		else:
			if "SetRe" in data:
				picaxe_config = ":01conf:\n\nM\x00" #chr(99)+chr(111)+chr(110)+chr(102)+chr(58)+chr(self.codes[0])+chr(self.codes[1])+chr(self.trans_method)+chr(self.handshake)
				#print picaxe_config
				self.ser.write(picaxe_config)
				print "sent config..."
			if "DATA" in data:
				data_array = list(data)
				id = data_array[4]
				value = data_array[5]
				checksum = data_array[6]
				return id, value, checksum
			else: return -1
			"""#print data_array
			for i in range(0, len(data_array)):
				if ord(data_array[i]) == 254:
					data_array[i] = "\n" # 254 is used instead of 10, so that it doesn't end the line during serial transmit, this turns it back.
			try:
				data_array.pop() # pops off the \n
				#checksum = ord(data_array.pop())
			except:
				pass
			check = 0
			for j in range(0, len(data_array)):
            			check += ord(data_array[j])
            		check += int(self.codes[0])*int(self.codes[1])
        		check = (check/4)
			check = int(math.floor(check))
			print check
			#print "CHECK:	" + str(check) + "CHECKSUM:	" + str(checksum)
        		num_data = []
			for i in range(0, len(data_array)):
        			num_data.append(ord(data_array[i]))
        		num_data.append(time.time())
			#print num_data
		
        		if check == checksum:
        			return num_data
        		else:
        			#return num_data
        			#print "incorrect check"
				if num_data == []:
        				self.get_input()
				else:
					return -1
			
			try:
				num_data = []
				for i in range(0, len(data_array)):
                        		num_data.append(ord(data_array[i]))
				num_data[len(num_data)-1] = time.time()
				print num_data
				#if num_data[0] > -1: # the picaxe uses unsigned numbering, so if it's either positive or NoneType. 
				#	print "dfdf" + str(num_data)
				return num_data
				#else:
				#	return -1
			except: #if no incoming data
				print "No data"
				return -1
			"""
