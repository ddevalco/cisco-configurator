#! python

import sys
import serial
import time
import string
import subprocess
import os
from statusmgr import StatusManager

def configure(port, tftp, host, dev, manager):
		
	#################
	# Set variables #
	#################	
	
	LOGIN_USERNAME = 'XXXXXXXX'
	LOGIN_PASSWD = 'XXXXXXXX'
	ENABLE_PASSWD = 'XXXXXXXX'
	
	
	# DO NOT TOUCH
	COM = (port - 1)
	TFTP_SERVER = tftp
	HOST = host
	sn = HOST.split('-')[0]
	manager.setHost(COM, HOST)
	
	




	#######################
	# DEVICE TYPE SECTION #
	#######################
	while True:
		# Select IOS based on user input	
		DEVICE = dev
		if DEVICE == 1: #2960S
			IOS_PATH = 'c2960s-universalk9-mz.122-53.SE1.bin'
			config_file = 'configs/' + HOST + '.txt'
			INTERFACE = 'Vlan1'
			break
		elif DEVICE == 2: #2911
			IOS_PATH = 'c2900-universalk9-mz.SPA.151-2.T1.bin'
			config_file = 'configs/' + HOST + '.txt'
			INTERFACE = 'GigabitEthernet0/0'
			break
		elif DEVICE == 3: #1941
			IOS_PATH = 'c1900-universalk9-mz.SPA.151-2.T1.bin'
			config_file = 'configs/' + HOST + '.txt'
			INTERFACE = 'GigabitEthernet0/0'
			break

# ADD MORE DEVICES WITH TEMPLATE BELOW
#		elif DEVICE == 4:	#PLACE TYPE DESCRIPTION HERE	
#			IOS_PATH = ''
#			config_file = ''
#			INTERFACE = ''
#			break

		

	try:
		ser = serial.Serial(COM)
	except:
		manager.setStatus(COM, 'Not connected')
		return 0
	
	
	ser.timeout = 0

	
	####################################################
	# Check to see if device is ready to be configured #
	####################################################
	
	manager.setStatus(COM, 'Waiting on Cisco device')
	while True:
		ser.flushInput()
		ser.write('\r\n\r\nno\n\n')
		time.sleep(1)
		out = ser.readlines()
		try:
			if(string.find(out[len(out)-1], '>')) > -1:
				break;
			if(string.find(out[len(out)-1], '#')) > -1:
				break;
		except:
			continue
		time.sleep(5)
			
	###############
	# Set up DHCP #
	###############

	
	
	manager.setStatus(COM, 'Setting up interface configurations')
	ser.write('conf t\nhostname device\ninterface ' + INTERFACE + '\nip add dhcp\nno shut\nend\n')
	
	time.sleep(5)
	
	########################################
	# Ensure device receives an IP Address #
	########################################
	
	manager.setStatus(COM, 'Waiting on DHCP...')
	if DEVICE == 1:
		while True:
			ser.flushInput()
			ser.write('show ip interface brief | i ' + INTERFACE + '\n')
			time.sleep(1)
			lines = ser.readlines()
			try:
				if string.find(lines[1], 'ass') == -1:
					IP_ADDR = (string.split(lines[1], ' '))[18]
					break;
			except:
				continue

	else:
		while True:
			ser.flushInput()
			ser.write('show ip interface brief | i ' + INTERFACE + '\n')
			time.sleep(1)
			lines = ser.readlines()
			try:
				if string.find(lines[1], 'ass') == -1:
					IP_ADDR = (string.split(lines[1], ' '))[9]
					break;
			except:
				continue
	
	time.sleep(5)
	
	manager.setIP(COM, IP_ADDR)
	
	###########################################
	# Ensure device can reach the TFTP server #
	###########################################
	manager.setStatus(COM, 'Testing connectivity to TFTP Server at ' + str(TFTP_SERVER))
	retry = 1
	while True:
		ser.flushInput()
		ser.write('ping ' + TFTP_SERVER + '\n')
		time.sleep(5)
		reply = ser.readlines()
		try:
			if int((string.split(reply[5], ' '))[3]) > 70:
				break;
		except:
			continue
		
		if retry < 6:
			retry = retry + 1
			manager.setStatus(COM, 'Testing TFTP connectivity, trial #' + str(retry))
		else:
			manager.setStatus(COM, 'Can\'t reach TFTP server. Thread stopped.')
			sys.exit(0)
		time.sleep(3)
		
	manager.setStatus(COM, 'Device can reach the TFTP Server.')
	
	################
	# Format flash #
	################
	
	manager.setStatus(COM, 'Formatting flash...')
	ser.flushInput()
	ser.write('format flash:\n\n\n')
	time.sleep(5)
	while True:
		out = ser.readline()
		if len(out) == 0:
			time.sleep(3)
			ser.flushInput()
			ser.write('\n\n')
		else:
			if string.find(out, 'device') > -1:
					break
			time.sleep(.5)
		
	################
	# Download IOS #
	################
	
	manager.setStatus(COM, 'Downloading IOS: ' + IOS + '...')
	retry = 1

	try:
		while True:
			ser.write('\ncopy tftp://' + TFTP_SERVER + '/' + IOS_PATH + ' flash:\n\n\n')
			sec = 50
			while True:
				if sec > 10:
					sec = sec - 10
				time.sleep(sec)
				if not ser.readlines():
					break
					
			# Verify IOS downloaded to flash
			time.sleep(1)
			ser.write('\n\n')
			ser.flushInput()
			ser.write('dir flash:\n')
			time.sleep(1)
			out = ser.readlines()
			found = False
			for x in out:
				if string.find(x, '.bin') > -1:
					found = True
			
			if found == True:
				break

			if retry < 4:
				manager.setStatus(COM, 'IOS did not download to flash. Retrying... (Attempt ' + \
																		str(retry) + ')') 
				retry = retry + 1
			else:
				manager.setStatus(COM, 'Cannot download IOS. Thread stopped.')
				sys.exit(0)
	except:
		manager.setStatus(COM, 'Error received at IOS install. Thread stopped.')
		sys.exit(0)
	
	manager.setStatus(COM, 'IOS has been updated to flash.')
	manager.setStatus(COM, 'Downloading configuration for ' + HOST + '...')
	
	#########################################
	# Download config file from TFTP Server #
	#########################################
	
	retry = 1
	while True:
		ser.write('\ncopy tftp://' + TFTP_SERVER + '/' + config_file + ' start\n\n\n')
		time.sleep(10)
		ser.write('\r\n\r\n')
		ser.flushInput()
		time.sleep(3)
		ser.flushInput()
		ser.write('show startup-config\n')
		time.sleep(1)
		out = ser.readlines()	
		try:
			if string.find(out[1], 'not present') == -1:
				break;
		except:
			continue
		
		if retry < 4:
			manager.setStatus(COM, 'Cannot download ' + config_file + \
					' from TFTP Server.\nRetrying... (Attempt ' + str(retry) + ')')
			retry = retry + 1
		else:
			manager.setStatus(COM, 'Cannot download config file. Thread stopped.')
			sys.exit(0)
	
	ser.write('\xcc\xcc\xcc\r\n\r\n')
	manager.setStatus(COM, 'Configuration copied to startup-config.')
	
	##########
	# Reboot #
	##########
	while True:
		ser.flushInput()
		ser.write('\n')
		time.sleep(1)
		out = ser.readlines()
		try:
			if(string.find(out[len(out)-1], '>')) > -1:
				ser.write('en\r\n')
				break;
			if(string.find(out[len(out)-1], '#')) > -1:
				break;
		except:
			continue
	
	
	manager.setStatus(COM, 'Reloading device.')
	ser.write('reload\r\n\r\n\r\n\r\n')
	
	sec = 120
	while True:
		time.sleep(sec)
		if not ser.readlines():
			break;
		if (sec > 30):
			sec = sec - 30
		else:
			sec = 10
	
	manager.setStatus(COM, 'Device has reloaded.')
	
	
	#######################################
	# Gain access to Privileged Exec mode #
	#######################################
	while True:
		ser.write('\r\n')
		
		while True:
			time.sleep(1)
			out = ser.readlines()
			try:
				if string.find(out[len(out)-1], 'Username') > -1:
					manager.setStatus(COM, 'Attempting initial login...')
					break
			except:
				continue
		
		# Initial login credentials
		ser.write(LOGIN_USERNAME)
		ser.write('\x0d')
		time.sleep(0.5)
		ser.readlines()
		ser.write(LOGIN_PASSWD)
		ser.write('\x0d')
		time.sleep(2)
		
		found = False
		while found == False:
			ser.write('\r\n')
			out = ser.readlines()
			print out
			for x in out:	
				if string.find(x, '>') > -1:
					manager.setStatus(COM, 'Entered User Exec mode.')
					found = True
					break
					
					
		if found == True:
			break
		
		manager.setStatus(COM, 'Failed login. Sleeping, then trying again.')
		time.sleep(10)
	
	# Enable secret credentials
	ser.write('en')
	ser.write('\x0d')
	time.sleep(1)
	ser.write(ENABLE_PASSWD)
	ser.write('\x0d')
	time.sleep(2)
	
	found = False
	while found == False:
		out = ser.readlines()
		for x in out:
			if string.find(x, '#') > -1:
				manager.setStatus(COM, 'Entered Priv Exec mode.')
				found = True
				break

	################################
	# Generate crypto keys for SSH #
	################################
	
	manager.setStatus(COM, 'Generating crypto keys...')
	ser.write('conf t\ncrypto key gen rsa g m 1024\n\n\n')
	time.sleep(3)
	ser.write('end\nwrite mem\n\n\n')

	manager.setStatus(COM, 'Done. Log in and verify configuration!')
	ser.close()
	
	subprocess.call(['putty.exe', 'COM' + str(COM + 1), '-serial'])
	