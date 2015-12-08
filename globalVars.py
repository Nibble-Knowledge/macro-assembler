#!/usr/bin/python

#global variables

	#macro memory used. Added so we can declare the right quantity.
	#altered in replaceLabels, if macro memory is needed.
memUsed = 0

	#Base Address Offset, to be set to default or grabbed from first file
BAddr = 1024

	#boolean variable to keep track of program structure.
	#helps enforce the rule about no instructions after data.
DataFields = False



	#List, treated as a queue, of files to handle
FList = []
FIndex = 0


