#! python

import sys
import serial
import time
import string
import os
import threading
from optparse import OptionParser, OptionGroup

# My scripts, dependent
from statusmgr import StatusManager
from autoconfig import configure

def main():

	###############################
	# Set up command line options #
	###############################
	parser = OptionParser(usage='usage: %prog [options]')
	parser.add_option('-f', '--file', action='store_true', dest='file', 
						help='designate file of COM - Hostname pairs (default keys.csv')


	(options, args) = parser.parse_args()
	
	####################
	# Assign variables #
	####################
	
	
	# DO NOT TOUCH
	# Manage status of each COM port
	manager = StatusManager()

	if options.file:
		if len(args) < 3:
			parser.print_help()
			sys.exit(0)
		file = sys.argv[2]
	else:
		file = 'settings.csv'
		
	
	# Read in COM HOST pairs
	f = open(file, 'r')
	lines = f.readlines()
	f.close()

		
		
	os.system('mode con cols=65 lines=50')
	############
	# Greeting #
	############
	sys.stdout.write('\n\n          .u:o. -c:o.  ex::u.    .czeez* .edB$ e@$$eu\n')
	sys.stdout.write('      e$MMMMMNu^$MMMb.#BMMM$c $MMM8P.d$RM$F4RMMMMMMRb\n')
	sys.stdout.write('      A$MMMMMMMMRb^$MMMMb^$MMMP MMMMF4$MMM8"dRMMMMMMMMMN\n')
	sys.stdout.write('      zMM8M***M$8M$.#8MMM$.$8M&J$M$%$RMM8*.$R8$#"""""BMM\n')
	sys.stdout.write('      $$".e@Rmu. "*M"    \'    ^^             .o$$RMM$c\'$\n')
	sys.stdout.write('      $.$RMMMMMM$$$$ dRRRRRRRRRR$$MMMMMMRL\'$$RMMMMMMMM$.\n')
	sys.stdout.write('      .$MMMMMMMMM$" $RMMMMMMMMMMMMMMMMMMMMb ^4$MMMMMMMM$\n')
	sys.stdout.write('      JMMMM$$**" ..$MMMMMMMMMMMMMMMMMMMMMMM$.:c  "***$MM\n')
	sys.stdout.write('      $M"..oenR$".$MMMMMMMMMMMMMMMMMMMMMMMMM$.*$$MMMRc.*\n')
	sys.stdout.write('      * d$MMMM$"u$MMMMMMMMMMMMMMMMMMMMMMMMM8MRc"$MMMMM$b\n')
	sys.stdout.write('      .$RMMM$# J$MF       "MMMMMMMMM        4M$b "$MMMM$\n')
	sys.stdout.write('      dMM8P"  dMMM$ $M8P4 4MMMMMMMMM \'L"$M$ JMMMF  "*88M\n')
	sys.stdout.write('      $$P\d$$ $MMMM$L..d$r4MMMMMMMMM <$$u.e$RMMMF $M$c"$\n')
	sys.stdout.write('      $ zRMM& ^8MMMMMMMMMF\'MMMMMMMMM 4MMMMMMMMMG  $MMM$r\n')
	sys.stdout.write('       $RMMMF$f)MMMMMMMMMF\'MMMMMMMMM 4MMMMMMMMMF.$\'$MMMM\n')
	sys.stdout.write('      \'MMM$FJR$ $MMMMMMMMF4MMMMMMMMM 4MMMMMMMM$ $Rh^$MMM\n')
	sys.stdout.write('      AMM8\dRMMF RMMMMMMM 4MMMMMMMMM  MMMMMMM$".MMMRb$MM\n')
	sys.stdout.write('      AM$.$MMMMF.3MMMM$P*-\'*********- "*NMMMM*..RMMMM$\'$\n')
	sys.stdout.write('      AP.$RMMM$:$ $M$".oM$.\'$RRRRR$".d$5u\'*M$ $$?RMMMM$\'\n')
	sys.stdout.write('      $ $MMMM$\$Rb\'P eMMMMM$c"$M8# dRMMMMRc"F4MMb^$MMMMb\n')
	sys.stdout.write('       $RMMMPzRMM!  eRMMMMMMR$c" dRMMMMMMMR  \'MMMR.?$MM$\n')
	sys.stdout.write('       $M8$ $MMMM"x $MMMMMMMMMM ?MMMMMMMMM$ 3\'$MMM$b\'$MM\n')
	sys.stdout.write('      ARM$.$RMMMP $$\'BMMMMMMMMM 4MMMMMMMM8P4$$ $MMMM$.$M\n')
	sys.stdout.write('      A$F4RMMMMf $RM  *88MMM88M J8MM888$$\ @MMMr5MMMM$.$\n')
	sys.stdout.write('       $ $RMM8P.$MMMF?b.                z$F$MMMMc3BMMM$\'\n')
	sys.stdout.write('        4MMMM$-$RMM8F4MM$ \'8MMMMMMMM$ dRMM$#8MMM$r#8MMM.\n')
	sys.stdout.write('       4MMM$.$MMMM$ RMMM$ 3MMMM$ 8MMM\n')
	sys.stdout.write('         $MM$\'MMMMP zRMMM$ .\'**4P*".$ $MMMM$\'$MMMM $MM$\n')
	sys.stdout.write('         4MMC\'MMMM$:$MMMMPoM$b   .@$M$$MMMMRL^$MMMF$M8\n')
	sys.stdout.write('          "$$\'MMM$\$MMMM$ MMMM$.4RMMM$r$MMMMRr*MMMN$$"\n')
	sys.stdout.write('           \'N\'$MM$4$MMMMF$MMMMM$$RMMMM$4$MMMM$$MMM @\n')
	sys.stdout.write('              #$MN4MMMMMF$MMMMM$#MMMMMM RMMMM$$M$F\n')
	sys.stdout.write('               ?$$.$MMMMF$MMMMMF RMMMMM $MMMM\$MP\n')
	sys.stdout.write('                 *$\'$MMMb3MMMMM  RMMMMNJRMMNFJ*\n')
	sys.stdout.write('     LEONIDAS        #88$L#8MMMr RMMM$z$M8$"\n')
	sys.stdout.write('      Cisco            ^*$P/*B8$$R8M"zP*"\n')
	sys.stdout.write('   Configurator  \n')
	sys.stdout.write('    July, 2013\n\n\n')

	
	for line in lines:
		if line[0] == '#' or line == '\n':
			continue
		
		line = line.strip('\n')
		if line.split(',')[0] == '':
			continue
		else:
			port = int(line.split(',')[0].strip(' ').strip('\n'))
		if line.split(',')[1] == '':
			continue
		else:
			host = line.split(',')[1].strip(' ').strip('\n')
		if line.split(',')[2] == '':
			continue
		else:
			type = int(line.split(',')[2].strip(' ').strip('\n'))
			if type < 1 or type > 3:
				continue
			
		
		manager.addon(port, host)
		t = threading.Thread(target=configure, args=(port, tftp, host, type, manager))
		t.start()
	print 'Ctrl-C will exit. Status updates every 5 sec.'

	time.sleep(5)

	while True:
		os.system('cls')
		manager.printAll()
		time.sleep(5)
		
if __name__ == '__main__':

	try:
		main()
	except KeyboardInterrupt:
			
		print('\nCheck your device configurations, I will not\n' + \
				'be held responsible for misconfigurations.')
		sys.exit(0)
