#! python
import sys
import string


###################################################################
#						StatusManager							  #
###################################################################
# Class to update user at which part of the configuration         #
# process each port is at. This class contains each ports status, #
# hostname, and IP Address if applicable. This allows us to pull  #
# status updates from the ports even if the ports are busy.       #
###################################################################
class StatusManager(object):


	def __init__(self):
		self.status = {}
		self.ip_addr = {}
		self.host = {}
	
	def addon(self, port, host):
		port = port - 1
		self.status[port] = 'Not connected'
		self.host[port] = host
		self.ip_addr[port] = '0.0.0.0'
		
	def setStatus(self, port, string):
		self.status[port] = string
		
		
	def setIP(self, port, ip):
		self.ip_addr[port] = ip
		
	def setHost(self, port, hn):
		self.host[port] = hn

	
	def getStatus(self, port):
		return self.status[port]
	
	def getIP(self, port):
		return self.ip_addr[port]
		
	def getHost(self, port):
		return self.host[port]
		
		
	def printAll(self):
		print '\n Current Status:' 
		for port in self.host:
			if (port == 0):
				continue
			elif (self.status[port] != 'Not connected'):
				sys.stdout.write('COM' + str(port + 1) + ': ' + self.status[port] + '\n')
				sys.stdout.write('   ' + self.getHost(port) + ' - ' + self.getIP(port) + '\n\n')
		
		# Make COM1 list last
		try:
			if (self.status[0] != 'Not connected'):
				sys.stdout.write('COM1:   ' + self.status[0] + '\n')
				sys.stdout.write('   ' + self.getHost(0) + ' - ' + self.getIP(0) + '\n')
		except:
			pass








		