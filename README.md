cisco-configurator
==================

This is a set of Python scripts created to automatically set up Cisco equipment with Windows. 

Prerequsites
-------------
- Install Python 2.7 on Windows
- Set up Login username and password along with enable passwords in autoconfig.py
- Have a TFTP server ready (look at DEVICE TYPE SECTION in autoconfig.py for directory layout)
- Place a putty.exe in the same folder as the python files
- Buy a PCI adapter for multiple serial ports such as: http://www.amazon.com/StarTech-com-PEX8S952-Native-Express-Adapter/dp/B001VSR9TK

Use
------------
- Edit the settings.csv file to prepare the Serial port to Configuration mapping
- Run "python configurator.py"

Future
-----------
I don't plan on making any changes unless requested. The scripts have been set in a way that
basic changes should be relatively easy to implement with a general knowledge of Python.
