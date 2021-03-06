#! /usr/bin/python2

import sys
import serial

log_file = "log.txt"

logi = 0
logautosave = 100
logtext = ""

correct_counter = 0
error_counter = 0

# Saves to the log file.
def log(entry, forcesave=False):
    global logi, logtext, logautosave, log_file
    print entry
    logtext += entry + "\n"
    logi+=1
    if (logi > logautosave) or forcesave:
        # Auto saves, encase of interupt.
	try:
        	f = open(log_file, "r")
        	pre_logtext = f.read()
		f.close()
	except: pre_logtext = ""
        logtext = pre_logtext + logtext
	f = open(log_file, "w")
        f.write(logtext)
        f.close()
        logtext = ""

def run_test(length, port, bord):
    global correct_counter, error_counter
    print "Starting test for " + str(length) + " Transmissions..."
    ser = serial.Serial(port, bord, timeout=2)
    for i in range(0, length):
        data = ser.readline()
        if data == "":
        	#missed packet.
        	missed = True
        	log("Missed packet")
        else: missed = False
        # Verify data
	data = data.split("\n")[0]
        data_array = list(data)
        try: checksum = ord(data_array.pop())
	except: checksum=255
        check = 0
	try:
        	for j in range(0, len(data_array)):
            		check += ord(data_array[j])
        	check /= len(data_array)
	except: pass
	if not missed:
        	if check == checksum:
            		correct_counter +=1
            		log("Got serial input '" + data + "'. Verified correct.")
        	else:
            		error_counter +=1
            		log("Got serial input '" + data + "'. Contains Error.")
    print "!!!! COMPLETE: SUMMARY AS FOLLOWS !!!!"
    summary = "Total errors: " + str(error_counter) + "\n"
    summary += "Total errors percentage: " + str(float(error_counter) / float((error_counter+correct_counter))) + "\n"
    summary += "Successful: " + str(correct_counter) + "\n"
    summary += "Successful percentage: " + str(float(correct_counter) / float(error_counter+correct_counter))+ "\n"
    summary += "Lost packets: " + str(length - (correct_counter + error_counter)) + "\n"
    summary += "Lost packets percentage: " + str((float(length) - float(correct_counter + error_counter))/float(length)) + "\n"
    summary += "Lost packets + errors: " + str(error_counter + (length - (correct_counter + error_counter))) + "\n"
    summary += "Lost packets + errors percentage: " + str(float((error_counter + (length - (correct_counter + error_counter))))/float(length)) + "\n"
    log(summary, forcesave=True)
    print "Done! Exiting."

def show_help():
    print "\n"
    print "Transtest help:"
    print "\n"
    print "This programme is designed to test serial input from radio transmitters for errors."
    print "The serial in data should be formatted as so: "
    print "<var1>,<var2>,<var3>,<as many as you want>,<checksum>"
    print "where the check sum is the average of all variables (mean)"
    print "\n"
    print "Options:"
    print "-help: this."
    print "-n=X: The number of times to read serial input."
    print "-log='file name of outputed log file': Where to save the log file. default=log.txt"
    print "-asave=X: Every X times it auto-saves the log file, encase of an interrupt, default=100"
    print "-port=X: The serial port, eg: /dev/ttyS0"
    print "-bord=X: bord rate, eg: 2400"
    print "\n"

def optionshandler():
    global logautosave, log_file
    options = sys.argv
    for i in range(0, len(options)):
        if options[i] == "-help":
            show_help()
        if "-n" in options[i]:
            test_number = options[i].split("=")[1]
        if "-log" in options[i]:
            log_file = options[i].split("=")[1]
        if "-asave" in options[i]:
            logautosave = options[i].split("=")[1]
        if "-port" in options[i]:
            port = options[i].split("=")[1]
        if "-bord" in options[i]:
            bord = options[i].split("=")[1]
    try:
    	run_test(int(test_number), port, int(bord))
    except:
        print "Error, have you given an n, port and bord? If so check pyserial is installed."
        print "For help, use transtest.py -help"

optionshandler()
