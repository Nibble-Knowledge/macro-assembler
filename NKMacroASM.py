#!/usr/bin/python

# Naomi Hiebert coded this



import string
import sys
import os



#import global variables
import globalVars

import macroExpand





	#Buffer for output instructions
IBuffer = []

	#Buffer for output data
DBuffer = []



# I know it looks weird having the main function hide
# all the way down here, but it avoids the need to
# force the interpreter to load all the other stuff
# first. Besides, a good main function is usually
# pretty sparse.

#main function

#parse argument vector
if len(sys.argv) < 2:
	print "no input file specified!"
	quit()
if len(sys.argv) < 3:
	print "no output file specified!"
	quit()

#Start the queue
globalVars.FList.append(sys.argv[1])

#open the appropriate files
outFile = open(sys.argv[2], "w")

#deal with files
while globalVars.FIndex < len(globalVars.FList):
	
	#first file breaks, everything breaks
	#other files break, not the worst thing
	try:
		inFile = open(globalVars.FList[globalVars.FIndex], "r")
	except OSError:
		if FIndex > 0:
			print "Serious exception: Included file not opened! " + globalVars.FList[gobalVars.FIndex] + '\n'
			print "Proceeding with other files. Output may not be valid.\n"
		else:
			print "Fatal exception: Base file not opened!"
			raise 

	#keep enforcing the organisation with files, but not between them.
	globalVars.DataFields = False

	#comments good
	DBuffer.append("\n;Start of data from " + globalVars.FList[globalVars.FIndex] + "\n")
	IBuffer.append("\n;Start of code from " + globalVars.FList[globalVars.FIndex] + "\n")
	
	#use the functions we defined above
	for line in inFile.readlines():
		expandedLine = macroExpand.expandline(line.split())
		for expLine in expandedLine:
			if(globalVars.DataFields):
				DBuffer.append(expLine)
			else:
				IBuffer.append(expLine)
	
	#comments foamy
	DBuffer.append("\n;End of data from " + globalVars.FList[globalVars.FIndex])
	IBuffer.append("\n;End of code from " + globalVars.FList[globalVars.FIndex])

	#housekeeping
	globalVars.FIndex += 1
	inFile.close()

#Add the one line of INF header that we care about
outFile.write("INF " + str(globalVars.BAddr) + '\n')

#dump the buffers
for ILine in IBuffer:
	outFile.write(ILine + '\n')

outFile.write(";Start of data sections")

for DLine in DBuffer:
	outFile.write(DLine + '\n')

#declare macro scratch space
if globalVars.memUsed > 0:
	outFile.write("\n;memory space used by macros\n")
	outFile.write("macro: .data " + str(globalVars.memUsed) + "\n\n")

#clean up after ourselves
outFile.close()

#done!



		

