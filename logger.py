#! /usr/bin/python2

# this script is designed to log away data to a server.
# to use with your other scripts, import and use the 'log' function with
# entry parameter.
# this will also automatic collect runtime information, as well as that 
# you pass it
# to get runtime information you must set it as a cron job
# for server upload, modify the following variables and make sure the 
# pub key of this device is in authenicated keys file on server

server = "128.199.181.173" # domain/address of server
user = "root" # what the logger will login as
path = "/var/www/html/resource/datahandling/logs/" # where to place log files on server.
