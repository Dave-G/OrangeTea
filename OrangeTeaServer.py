# OrangeTeaServer - Server program to host remote OrangeTeaClient instances
# Created by David Gedarovich
# http://www.github.com/Dave-G
# gedarovich@hotmail.com
# Updated 1/27/12
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

# Server header
print "Note: clients must be given your IP address and port to connect."
# Ask for Welcome message and IP/Port, provide them if not given
welcome = raw_input("Enter a welcome message to display to clients: ")
if (welcome == ''):
	print "Invalid input. Defaulting to: Welcome to OrangeTea!"
	welcome = "Welcome to OrangeTea!"
port = raw_input("Enter a port to bind: ")
# Make sure the input can be converted to an integer
if (checkInt(port)):
	port = int(port)
else:
	print "Invalid input. Defaulting to: 23456."
	port = 23456
os.system('pause')
# Set up variables
IP = ''
address = (IP, port)
msgLog = list()
# Set up server
try:
	s = socket(AF_INET, SOCK_STREAM)
	s.bind(address)
	s.listen(5)
	os.system('cls')
	os.system('ipconfig')
except:
	print "Error in configuring server."
	os.system('pause')
	exit()
print "\nServer established on Port " + str(port) + ".\n"
# Run server
while 1:
	print "Waiting for connection"
	client, addr = s.accept()
	print "Connection from: ", addr[0], "on port:", addr[1]
	client.send(welcome)
	while 1:
		try:
			data = client.recv(1024)
		except:
			print "Connection has been lost."
			break
		# End connection if bad data (or disconnect)
		if (not data):
			break
		# Notify if receiving a hashed string 
		# (32 chars in MD5)
		if (len(data) == 32):
			print "Hashed string(MD5) detected."
		# (40 chars in SHA-1)
		if (len(data) == 40):
			print "Hashed string(SHA-1) detected."
		# Send file if Client types /get <filename>
		if (data[0:4] == '/get'):
			print "Client has requested file for download: " + data[5:]
			# Catch errors in file sending
			try:
				f = open(data[5:], 'r')
				print "Sending file to Client..."
				file = f.read()
				client.send(file)
				if (not file):
					break
				f.close()
			except:
				"Error in sending file."
		# Send file if Client types /wget <filename>
		if (data[0:5] == '/wget'):
			print "Client has requested file for read: " + data[6:]
			# Catch errors in file sending
			try:
				f = open(data[6:], 'r')
				print "Sending file to Client..."
				file = f.read()
				client.send(file)
				if (not file):
					break
				f.close()
			except:
				"Error in sending file."
		# Receive file if Client types /send <filename>
		if (data[0:5] == '/send'):
			print "Client has requested to send file: " + data[6:]
			client.send("File transfer accepted.")
			print "Receiving file"
			file = client.recv(1000000)
			if (not file):
					break
			# Catch errors in file reception
			try:
				f = open('C:\myfile.txt', 'w')
				f.write(file)
				f.close()
				print "File saved to C:\\myfile.txt"
			except:
				"Error in receiving file."
		# Perform system command if Client types /sys <command>
		if (data[0:4] == '/sys'):
			print "Client has issued system command: " + data[5:]
			try:
				report = os.popen(data[5:]).read()
				print report
				if (not report):
					client.send('Command completed.')
				else:
					client.send(report)
			except:
				print "Error in executing command."
		# Close connection if client exits via command
		if (data == '/exit'):
			data = "Client (IP: " + str(addr[0]) + ", Port: " + str(addr[1]) + ") has exited the session."
			print data
			msgLog.append(data)
			break
		else:
			# Don't show/log empty messages
			if (data != ' '):
				print "(" + time.asctime(time.localtime())[11:16] + ") " + "Client/> " + data
				# Add the message to the log
				msgLog.append(data)
	# Wait for a new client if one ends the session
	client.close()
s.close()