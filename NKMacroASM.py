#!/usr/bin/python

# Naomi Hiebert coded this

import string
import sys
import os

#hardcoded data - for identifying macro types
	
	#native NK opcodes so we can identify them
opcodes = ["ADD", "NND", "LOD", "STR", "HLT", "CXA", "NOP", "JMP"]

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

	elif isBinaryMacro(splitline):
		expLine.extend(expandBinaryMacro(splitline))

	else:
		syntaxfail(splitline)

	return expLine

#boolean functions - for identifying macros and syntax errors


#blank or comment lines fall through unchanged - call first
def isBlankOrComment(splitline):
	if len(splitline) == 0 or splitline[0][0] == '#':
		return True
	else:
		return False

#checks if it's native ASM. Call after isBlankOrComment, but before checking
#for actual macros
def isNativeASM(splitline):
	if len(splitline) == 2 and splitline[0] in opcodes:
		return True
	else:
		return False

#if it's not a comment or native ASM, anything with 2 tokens is an acc macro
def isAccMacro(splitline):
	if len(splitline) == 2 and splitline[0] in accMac and splitline[1] == "ACC":
		return True
	else:
		return False

#if not a comment or native ASM, anything with 4 tokens is a unary macro
def isUnaryMacro(splitline):
	if len(splitline) == 4 and splitline[0] in unaMac and splitline[2] == "INTO":
		return True		
	else:
		return False

#if not a comment, anything with 5 tokens is a binary macro
def isBinaryMacro(splitline):
	if len(splitline) == 5 and splitline[0] in binMac and splitline[3] == "INTO":
		return True
	else:
		return False


def syntaxfail(errorline):
	raise Exception("Syntax Error", " ".join(errorLine))

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

#Takes: a split line
#Returns: a list of (joined) lines
def expandUnaryMacro(inMac):
	outlines = []
	op1 = inMac[1]
	dest = inMac[3]

	for line in unaMac[inMac[0]].splitlines():
		splitline = line.split()
	
		#replace our placeholder labels with the input ones
		splitline = replaceLabels(splitline, "$op1", op1)
		splitline = replaceLabels(splitline, "$dest", dest)

		#recursively expand the resulting line
		outlines.extend(expandline(splitline))
	return outlines

#Takes: a split line
#Returns: a list of lines
def expandBinaryMacro(inMac):
	outlines = []
	op1 = inMac[1]
	op2 = inMac[2]
	dest = inMac[4]

	for line in binMac[inMac[0]].splitlines():
		splitline = line.split()
	
		#replace our placeholder labels with the input ones
		splitline = replaceLabels(splitline, "$op1", op1)
		splitline = replaceLabels(splitline, "$op2", op2)
		splitline = replaceLabels(splitline, "$dest", dest)

		#recursively expand the resulting line
		outlines.extend(expandline(splitline))
	return outlines

#Takes: a split line,
#		the placeholder (starts with $ usually) label to replace
#		the new label (maybe with [offset]) to replace it with
#Also note that the placeholder in the line may also have an offset
#Returns: a split line
def replaceLabels(splitline, oldlabel, replabel):
	outline = []

	for token in splitline:
		if token.startswith(oldlabel):

			#default values, if no offset found
			oldoffset = 0
			repoffset = 0

			#get the offset from the replacement, if necessary
			if '[' in replabel and ']' in replabel:
				repoffset = replabel[replabel.index('[') + 1 : replabel.index(']')]
				repoffset = int(repoffset, 16)

			#and from the old label, if necessary
			if '[' in token and ']' in token:
				oldoffset = token[token.index('[') + 1 : token.index(']')]
				oldoffset = int(oldoffset, 16)
			
			#add them together
			newoffset = oldoffset + repoffset

			#smash together the new token
			if '[' in replabel:
				newtoken = replabel[:replabel.find('[')] + '[' + hex(newoffset)[2:] + ']'
			else:
				newtoken = replabel + '[' + hex(newoffset)[2:] + ']'

			#put it in the output line
			outline.append(newtoken)
		else:
			#not the label we're looking for
			outline.append(token)

	return outline


#macros for expansion

#Accumulator-based Macros
accMac = dict()

accMac["NOT"] = """\
NND lit[F]"""

accMac["NEG"] = """\
NOT ACC
INC ACC"""

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

accMac["LOGNOT"] = """\
ADD lit[F]
CXA 0
NND lit[1]
NND lit[1]
NND lit[F]"""


#unary operation macros

unaMac = dict()

unaMac["MOV"] = """\
LOD $op1[0]
STR $dest[0]"""

unaMac["MOV8"] = """\
LOD $op1[0]
STR $dest[0]
LOD $op1[1]
STR $dest[1]"""

unaMac["MOV16"] = """\
LOD $op1[0]
STR $dest[0]
LOD $op1[1]
STR $dest[1]
LOD $op1[2]
STR $dest[2]
LOD $op1[3]
STR $dest[3]"""

unaMac["MOV32"] = """\
LOD $op1[0]
STR $dest[0]
LOD $op1[1]
STR $dest[1]
LOD $op1[2]
STR $dest[2]
LOD $op1[3]
STR $dest[3]
LOD $op1[4]
STR $dest[4]
LOD $op1[5]
STR $dest[5]
LOD $op1[6]
STR $dest[6]
LOD $op1[7]
STR $dest[7]"""

unaMac["MOV64"] = """\
LOD $op1[0]
STR $dest[0]
LOD $op1[1]
STR $dest[1]
LOD $op1[2]
STR $dest[2]
LOD $op1[3]
STR $dest[3]
LOD $op1[4]
STR $dest[4]
LOD $op1[5]
STR $dest[5]
LOD $op1[6]
STR $dest[6]
LOD $op1[7]
STR $dest[7]
LOD $op1[8]
STR $dest[8]
LOD $op1[9]
STR $dest[9]
LOD $op1[A]
STR $dest[A]
LOD $op1[B]
STR $dest[B]
LOD $op1[C]
STR $dest[C]
LOD $op1[D]
STR $dest[D]
LOD $op1[E]
STR $dest[E]
LOD $op1[F]
STR $dest[F]"""

unaMac["NOT"] = """\
LOD $op1
NOT ACC
STR $dest"""

unaMac["NEG"] = """\
LOD $op1
NEG ACC
STR $dest"""

unaMac["PROPCARR"] = """\
GETCARR ACC
ADD $op1
STR $dest"""

unaMac["NEG8"] = """\
NOT $op1 INTO $dest
NEG $op1[1] INTO $dest[1]
PROPCARR $dest INTO $dest"""


#binary operation macros

binMac = dict()

binMac["ADDC"] = """\
ADD $op1
STR macro[1]
GETCARR ACC
NOT ACC
STR macro[0]
LOD macro[1]
ADD $op1
STR $dest
GETCARR ACC
NOT ACC
NND macro[0]"""

binMac["ADD8"] = """\
LOD lit[0]
ADDC $op1[1] $op2[1] INTO $dest[1]
ADDC $op1[0] $op2[0] INTO $dest[0]"""



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
		

