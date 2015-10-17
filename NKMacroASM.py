#!/usr/bin/python

# Naomi Hiebert coded this

import string
import sys
import os

#hardcoded data - for identifying macro types
	
	#native NK opcodes
opcodes = ["ADD", "NND", "LOD", "STR", "HLT", "CXA", "NOP", "JMP"]

	#accumulator-based macros - only recognising two for now
accMacroCodes = ["NOT", "NEG", "GETCARR", "INC", "DEC", "LSHIFT", "LROT"]

#global variables

#output buffer - holds only fully macro-expanded code
output = []


# The real heart of the operation - identifies macros anywhere,
# including inside other macros! Tends to get called recursively
# since macros inside macros need to be expanded inside macros.

#Takes: a split line
#Returns: a list of (joined) lines

def expandline(splitline):
	expLine = []

	if isBlankOrComment(splitline): #the base case for non-code lines
		expLine.append(" ".join(splitline))

	elif isNativeASM(splitline):	#the base case for code lines
		expLine.append(" ".join(splitline))

	elif isAccMacro(splitline):
		expLine.extend(expandAccMacro(splitline))

	elif isUnaryMacro(splitline):
		expLine.extend(expandUnaryMacro(splitline))

	return expLine

#boolean functions - for identifying macros and syntax errors


def isBlankOrComment(splitline):
	if len(splitline) < 1:
		return True
	elif splitline[0][0] == '#':
		return True
	else:
		return False

def isNativeASM(splitline):
	if len(splitline) < 1:
		return False
	elif splitline[0] in opcodes:
		if len(splitline) == 2:
			return True
		else:
			syntaxfail(splitline)
	else:
		return False

def isAccMacro(splitline):
	if len(splitline) < 2:
		return False
	elif splitline[0] in accMacroCodes and splitline[1] == "ACC":
		#probably an acc macro
		if len(splitline) == 2:
			return True
		else:
			syntaxfail(splitline)
	else:
		return False

def isUnaryMacro(splitline):
	return False

def syntaxfail(errorline):
	raise Exception("Syntax Error", errorLine.join())


#replacement functions - expand those macros!


# the simplest expasion function, since no acc macro
# takes any arguments. Some might contain other macros
# though, so we still need to check

#Takes: a split line (as list of single-word strings)
#Returns: a list of (joined) lines (possibly a single-element list)
def expandAccMacro(inMac):
	outlines = []

	for line in accMac[inMac[0]].splitlines():
		outlines.extend(expandline(line.split()))
	return outlines




#macros for expansion

#Accumulator-based Macros
accMac = dict()

accMac["NOT"] = """\
NND lit[F]"""

accMac["NEG"] = """\
NOT ACC
ADD lit[1]"""

accMac["GETCARR"] = """\
CXA 0
NND lit[1]
NND lit[F]"""

accMac["INC"] = """\
ADD lit[1]"""

accMac["DEC"] = """\
ADD lit[F]"""

accMac["LSHIFT"] = """\
STR macro[0]
ADD macro[0]"""

accMac["LROT"] = """\
STR macro[0]
ADD macro[0]
STR macro[0]
GETCARR ACC
ADD macro[0]"""



#main function

if len(sys.argv) < 2:
	print "no input file specified!"
	quit()
if len(sys.argv) < 3:
	print "no output file specified!"
	quit()

inFile = open(sys.argv[1], "r")
print "input file opened: " + sys.argv[1]
outFile = open(sys.argv[2], "w")
print "output file opened: " + sys.argv[2]
	
for line in inFile.readlines():
	expandedLine = expandline(line.split())
	for expLine in expandedLine:
		outFile.write(expLine + "\n")

inFile.close()
outFile.close()
		

