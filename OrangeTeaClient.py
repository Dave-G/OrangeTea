# OrangeTeaClient - Client program to remotely control or communicate with an OrangeTeaServer
# Created by David Gedarovich
# http://www.github.com/Dave-G
# gedarovich@hotmail.com
# Updated 1/20/12
from socket import *
import time
import os
import hashlib

# Checks if the value can be converted to an integer
def checkInt(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

# Client header
print "Note: Your IP address and port are recorded upon connection."
# Ask for Name/IP/Port, provide them if not given
name = raw_input("Enter a name to display upon connection: ")
if (name == ''):
	print "Invalid input. Defaulting to: Anonymous."
	name = 'Anonymous'
IP = raw_input("Enter an IP to connect to: ")
if (IP == ''):
	print "Invalid input. Defaulting to: localhost."
	IP = 'localhost'
port = raw_input("Enter a port to connect to: ")
# Make sure the input can be converted to an integer
if (checkInt(port)):
	port = int(port)
else:
	print "Invalid input. Defaulting to: 23456."
	port = 23456
os.system('pause')
# Set address and socket for connection
address = (IP, port)
s = socket(AF_INET, SOCK_STREAM)
# Attempt connection
print "Connecting..."
try:
	s.connect(address)
except:
	print "Error in connecting."
	os.system('pause')
	exit()
os.system('cls')
# Greetings
print "Connected to:", address
welcome = s.recv(1024)
print welcome
s.send(name + " has connected.")
# Run client
while 1:
	data = raw_input("(" + time.asctime(time.localtime())[11:16] + ") " + name + "/>")
	# Default bad data to an empty space
	if not data:
		data = ' '
	# Client types /exit
	if (data == '/exit'):
		s.send('/exit')
		break
	# Client types /clear
	elif (data == '/clear'):
		os.system('cls')
	# Client types /hash md5
	elif (data[0:8] == '/hashmd5'):
		data = hashlib.md5(data[9:]).hexdigest()
		print "Sending hashed string: " + data
		s.send(data)
	# Client types /hash sha1
	elif (data[0:9] == '/hashsha1'):
		data = hashlib.sha1(data[9:]).hexdigest()
		print "Sending hashed string: " + data
		s.send(data)
	# Client types /help
	elif (data == '/help'):
		print "/exit -- exit gracefully and notify server"
		print "/clear -- clear all text on the screen"
		print "/hashmd5 <string> -- hash a string using MD5 to send to the server"
		print "/hashsha1 <string> -- hash a string using SHA-1 to send to the server"
		print "-- Note: hashing is done locally so data is safe from packet interception"
		print "/get <file path> -- outputs a file from the Server at given path"
		print "/wget <file path> -- downloads a file from the Server at given path"
		print "/send <file path> -- transfers a file to the Server from a given path"
		print "-- Note: file paths must be fully written. Ex: C:\\file.txt"
		print "/sys <command> -- executes a system command on the server"
	# Client types /get <path>
	elif (data[0:4] == '/get'):
		s.send(data)
		print "Receiving file..."
		try:
			file = s.recv(1000000)
			if (not file):
				break
			print file
		except:
			print "Error in receiving file."
	# Client types /wget <path>
	elif (data[0:5] == '/wget'):
		s.send(data)
		print "Downloading file..."
		try:
			file = s.recv(1000000)
			if (not file):
				break
			f = open('C:\myfile.txt', 'w')
			f.write(file)
			f.close()
			print "File downloaded to: C:\myfile.txt"
		except:
			print "Error in downloading file."
	# Client types /send <path>
	elif (data[0:5] == '/send'):
		s.send(data)
		print "Waiting for reply..."
		confirm = s.recv(1024)
		if (not confirm):
			break
		print confirm
		print "Sending file..."
		try:
			print data[6:]
			f = open(data[6:], 'r')
			file = f.read()
			print file
			s.send(file)
			f.close()
			print "File sent sucessfully."
		except:
			print "Error in sending file."
	# Client types /sys
	elif (data[0:4] == '/sys'):
		s.send(data)
		print "System command issued."
		report = s.recv(4096)
		print report
	else:
		try:
			s.send(data)
		except:
			print "Connection has been lost."
			os.system('pause')
			break
s.close()