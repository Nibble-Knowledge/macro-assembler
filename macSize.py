#!/usr/bin/python

#for parsing the argument vector
import sys

#make it more BASH-friendly
import errno

#The back end of the macro expander
import macroExpand

#The data structures holding the macro language

from asmDicts import opcodes


#Takes: a split line, assumed to be a syntactically valid mac4 statement
#Returns: an integer describing the number of assembly instructions
#			it expands into
def macroSize(splitInput):

	#Call the macro expander to give us the expanded form of the macro
	expLine = macroExpand.expandline(splitInput)
	lineCount = 0

	#Grep through the output, counting lines that hold actual assembly instructions
	for line in expLine:
		thisLine = line.split()
		if thisLine[0] in opcodes:
			lineCount += 1
	
	return lineCount

#Main function: Parses the argument vector, checks that it's been
#	given a valid opcode, gets the size, prints the size 
if __name__ == "__main__":

	#In this mode, we actually need the dictionaries of macros
	from accMacDict import accMac
	from unaMacDict import unaMac
	from binMacDict import binMac
	from jmpMacDict import jmpMac

	#The three actual variables we care about
	splitInput = []
	expLine = []
	count = 0

	#First error condition: No opcode given
	#Play dumb, say that no opcode equals zero length
	if len(sys.argv) < 2:
		print "0"
		quit()

	#If they explicitly mark an opcode as the accumulator version of the opcode
	if len(sys.argv) == 3 and sys.argv[2] == "ACC" and sys.argv[1] in accMac:
		splitInput = sys.argv[1:] 

	#If they give an opcode that is only valid as an accumulator macro
	elif sys.argv[1] in accMac and sys.argv[1] not in unaMac:
		splitInput = sys.argv[1:] + ["ACC"]

	#Unary macros - opcodes that can be either unary or ACC default to unary
	elif sys.argv[1] in unaMac:
		splitInput.append(sys.argv[1])
		splitInput.extend("arg1 INTO location".split())

	#Binary macros
	elif sys.argv[1] in binMac:
		splitInput.append(sys.argv[1])
		splitInput.extend("arg1 arg2 INTO location".split())

	#Jump macros
	elif sys.argv[1] in jmpMac:
		splitInput.append(sys.argv[1])
		splitInput.extend("arg1 arg2 TO location".split())

	#Error condition 2: They give us something that looks like an opcode,
	#but isn't valid
	else:
		print "No valid opcode detected!"
		quit(errno.EINVAL)

	#Call our externally-visible function to get the size
	count = macroSize(splitInput)

	#Output our results
	print count


