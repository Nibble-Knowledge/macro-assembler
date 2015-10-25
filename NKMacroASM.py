#!/usr/bin/python

# Naomi Hiebert coded this

import string
import sys
import os

#hardcoded data - for identifying macro types
	
	#native NK opcodes so we can identify them
opcodes = ["ADD", "NND", "LOD", "STR", "HLT", "CXA", "NOP", "JMP"]
unaryOpcodes = ["NOP", "CXA", "HLT"]
metaInstructions = ["INF", "PINF", "EPINF", "EINF", "BADR", "DSEC", "DNUM", "DSIZE"]

	#assembler-supported data type labels
dataTypes = [".data", ".ascii", ".asciiz"]

#global variables

	#macro memory used. Added so we can declare the right quantity.
	#altered in replaceLabels, if macro memory is needed.
memUsed = 0

	#boolean variable to keep track of program structure.
	#helps enforce the rule about no instructions after data.
DataFields = False


# The real heart of the operation - identifies macros anywhere,
# including inside other macros! Tends to get called recursively
# since macros inside macros need to be expanded inside macros.

#Takes: a split line
#Returns: a list of (joined) lines

def expandline(splitline):
	expLine = []

	if isFallthroughLine(splitline): #the base case - encompasses several other cases
		expLine.append(" ".join(splitline))

	elif isAccMacro(splitline):
		expLine.extend(expandAccMacro(splitline))

	elif isUnaryMacro(splitline):
		expLine.extend(expandUnaryMacro(splitline))

	elif isBinaryMacro(splitline):
		expLine.extend(expandBinaryMacro(splitline))

	elif isJumpMacro(splitline):
		expLine.extend(expandJumpMacro(splitline))

	else:
		syntaxfail(splitline)

	return expLine

#boolean functions - for identifying macros and syntax errors

#all the base cases return true on this line
def isFallthroughLine(splitline):
	if isBlankOrComment(splitline):
		return True
	elif isNativeASM(splitline):
		return True
	elif isSoleLabel(splitline):
		return True
	elif isData(splitline):
		return True
	elif isMetaData(splitline):
		return True
	else:
		return False


#blank or comment lines fall through unchanged
def isBlankOrComment(splitline):
	if len(splitline) == 0 or splitline[0][0] == '#' or splitline[0][0] == ";":
		return True
	else:
		return False

#checks if it's native ASM.
def isNativeASM(splitline):
	if len(splitline) == 2 and splitline[0] in opcodes:
		if DataFields:
			structurefail(splitline)
		return True
	elif len(splitline) == 1 and splitline[0] in unaryOpcodes:
		if DataFields:
			structurefail(splitline)
		return True
	else:
		return False

#checks if it fits the standard label syntax, alone on a line
def isSoleLabel(splitline):
	if len(splitline) == 1 and splitline[0][-1] == ':':
		return True
	else:
		return False

def isMetaData(splitline):
	if len(splitline) in [1,2] and splitline[0] in metaInstructions:
		return True
	else:
		return False

#checks if it's a data declaration, possibly with label
def isData(splitline):
	global DataFields
	if len(splitline) > 1 and splitline[0] in dataTypes:
		DataFields = True
		return True
	elif len(splitline) > 2 and splitline[1] in dataTypes:
		DataFields = True
		return True
	else:
		return False

#detects accumulator-based macros
def isAccMacro(splitline):
	if len(splitline) == 2 and splitline[0] in accMac and splitline[1] == "ACC":
		return True
	else:
		return False

#detects unary operation macros
def isUnaryMacro(splitline):
	if len(splitline) == 4 and splitline[0] in unaMac and splitline[2] == "INTO":
		return True		
	else:
		return False

#detects binary operation macros
def isBinaryMacro(splitline):
	if len(splitline) == 5 and splitline[0] in binMac and splitline[3] == "INTO":
		return True
	else:
		return False

#detects jump macros
def isJumpMacro(splitline):
	if len(splitline) == 5 and splitline[0] in jmpMac and splitline[3] == "TO":
		return True
	else:
		return False

#complains when it can't figure out what you're saying
def syntaxfail(errorline):
	raise Exception("Syntax Error!", " ".join(errorline))

#complains when you put data in front of instructions
def structurefail(errorline):
	raise Exception("Structural Error: Instructions cannot be placed after data fields!",
		" ".join(errorline))


#replacement functions - expand those macros!


# The simplest expasion function, since no acc macro
# takes any arguments. Some might contain other macros
# though, so we still need to check

#Takes: a split line (as list of single-word strings)
#Returns: a list of (joined) lines (possibly a single-element list)
def expandAccMacro(inMac):
	outlines = []

	for line in accMac[inMac[0]].splitlines():
		outlines.extend(expandline(line.split()))
	return outlines

# Really the only difference between unary and binary is
# the number of arguments. That's why the functions are
# almost identical.

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

# Frankly, this is no different from the operation macros.
# I just split them into different dictionaries for ease of
# coding and maintenance. The only cost of that decision was
# having to write this function, which is basically identical
# to the functions above.

#Takes: a split line
#Returns: a list of lines
def expandJumpMacro(inMac):
	outlines = []
	op1 = inMac[1]
	op2 = inMac[2]
	dest = inMac[4]

	for line in jmpMac[inMac[0]].splitlines():
		splitline = line.split()
	
		#replace our placeholder labels with the input ones
		splitline = replaceLabels(splitline, "$op1", op1)
		splitline = replaceLabels(splitline, "$op2", op2)
		splitline = replaceLabels(splitline, "$dest", dest)

		#recursively expand the resulting line
		outlines.extend(expandline(splitline))
	return outlines

# One of the more complex bits of code in this script, if only
# because of the amount of string operations involved. Takes 
# macros and part of their context, and replaces the $-marked
# placeholder tokens in the macros with the actual labels they
# should hold. Also does math on memory offsets, so we don't
# have to define a new label for each nibble of memory. Finally,
# keeps up the counter on the amount of memory used internal to
# the macros we're using. This allows us to declare only as much
# macro scratch space as we need.

#Takes: a split line,
#		the placeholder (starts with $ usually) label to replace
#		the new label (maybe with [offset]) to replace it with
#Also note that the placeholder in the line may also have an offset
#Returns: a split line
#Edits: global "memUsed" variable, if necessary
def replaceLabels(splitline, oldlabel, replabel):
	outline = []
	global memUsed

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

		#check if we're using macro memory. If so, we might need to 
		#expand our macro memory bank.
		if "macro[" in outline[-1]:
			macoffset = outline[-1][outline[-1].index('[') + 1 : outline[-1].index(']')]
			macoffset = int(macoffset, 16)
			if macoffset > memUsed:
				memUsed = macoffset

	return outline


#macros for expansion

#Accumulator-based Macros
accMac = dict()

accMac["NOT"] = """\
NND N_[F]"""

accMac["NEG"] = """\
NOT ACC
INC ACC"""

accMac["GETCARR"] = """\
CXA 0
NND N_[1]
NND N_[F]"""

accMac["GETCMP"] = """\
CXA 0
NND N_[8]
NND N_[F]"""

accMac["INC"] = """\
ADD N_[1]"""

accMac["DEC"] = """\
ADD N_[F]"""

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
ADD N_[F]
CXA 0
NND N_[1]
NND N_[1]
NND N_[F]"""


#unary operation macros - 4-bit versions

unaMac = dict()

unaMac["MOV"] = """\
LOD $op1[0]
STR $dest[0]"""

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

unaMac["INC"] = """\
LOD N_[1]
ADD $op1
STR $dest"""

unaMac["LSHIFT"] = """\
LOD N_[0]
ADD $op1
ADD $op1
STR $dest"""

unaMac["LROT"] = """\
LOD N_[0]
LSHIFT $op1 INTO $dest
GETCARR ACC
ADD $dest
STR $dest"""

#unary operation macros - longer versions

unaMac["MOV8"] = """\
MOV $op1[0] INTO $dest[0]
MOV $op1[1] INTO $dest[1]"""

unaMac["MOV16"] = """\
MOV8 $op1[0] INTO $dest[0]
MOV8 $op1[2] INTO $dest[2]"""

unaMac["MOV32"] = """\
MOV16 $op1[0] INTO $dest[0]
MOV16 $op1[4] INTO $dest[4]"""

unaMac["MOV64"] = """\
MOV32 $op1[0] INTO $dest[0]
MOV32 $op1[8] INTO $dest[8]"""

unaMac["NOT8"] = """\
NOT $op1[0] INTO $dest[0]
NOT $op1[1] INTO $dest[1]"""

unaMac["NOT16"] = """\
NOT8 $op1[0] INTO $dest[0]
NOT8 $op1[2] INTO $dest[2]"""

unaMac["NOT32"] = """\
NOT16 $op1[0] INTO $dest[0]
NOT16 $op1[4] INTO $dest[4]"""

unaMac["NOT64"] = """\
NOT32 $op1[0] INTO $dest[0]
NOT32 $op1[8] INTO $dest[8]"""

unaMac["NEG8"] = """\
NOT $op1 INTO $dest
NEG $op1[1] INTO $dest[1]
PROPCARR $dest INTO $dest"""

unaMac["NEG16"] = """\
NOT16 $op1 INTO $dest
INC16 $dest INTO $dest"""

unaMac["NEG32"] = """\
NOT32 $op1 INTO $dest
INC32 $dest INTO $dest"""

unaMac["NEG64"] = """\
NOT64 $op1 INTO $dest
INC64 $dest INTO $dest"""

unaMac["INC8"] = """\
LOD N_[1]
ADD $op1[1]
STR $dest[1]
PROPCARR $op1[0] INTO $dest[0]"""

unaMac["INC16"] = """\
INC8 $op1[2] INTO $dest[2]
PROPCARR $op1[1] INTO $dest[1]
PROPCARR $op1[0] INTO $dest[0]"""

unaMac["INC32"] = """\
INC16 $op1[4] INTO $dest[4]
PROPCARR $op1[3] INTO $dest[3]
PROPCARR $op1[2] INTO $dest[2]
PROPCARR $op1[1] INTO $dest[1]
PROPCARR $op1[0] INTO $dest[0]"""

unaMac["INC64"] = """\
INC32 $op1[8] INTO $dest[8]
PROPCARR $op1[7] INTO $dest[7]
PROPCARR $op1[6] INTO $dest[6]
PROPCARR $op1[5] INTO $dest[5]
PROPCARR $op1[4] INTO $dest[4]
PROPCARR $op1[3] INTO $dest[3]
PROPCARR $op1[2] INTO $dest[2]
PROPCARR $op1[1] INTO $dest[1]
PROPCARR $op1[0] INTO $dest[0]"""

unaMac["LSHIFT8"] = """\
ADD8 $op1 $op1 INTO $dest"""

unaMac["LSHIFT16"] = """\
ADD16 $op1 $op1 INTO $dest"""

unaMac["LSHIFT32"] = """\
ADD32 $op1 $op1 INTO $dest"""

unaMac["LSHIFT64"] = """\
ADD64 $op1[0] $op1[0] INTO $dest[0]"""

unaMac["LROT8"] = """\
LSHIFT8 $op1 INTO $dest
ADD $dest[1]
STR $dest[1]"""

unaMac["LROT16"] = """\
LSHIFT16 $op1 INTO $dest
ADD $dest[3]
STR $dest[3]"""

unaMac["LROT32"] = """\
LSHIFT32 $op1 INTO $dest
ADD $dest[7]
STR $dest[7]"""

unaMac["LROT64"] = """\
LSHIFT64 $op1 INTO $dest
ADD $dest[F]
STR $dest[F]"""

#binary operation macros, 4-bit

binMac = dict()

binMac["ADD"] = """\
LOD $op1
ADD $op2
STR $dest"""

binMac["ADDC"] = """\
ADD $op1
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2
STR $dest
CXA
NND N_[1]
NND macro[0]"""

binMac["SUB"] = """\
LOD $op1
NEG ACC
ADD $op2
STR $dest"""

binMac["NAND"] = """\
LOD $op1
NND $op2
STR $dest"""

binMac["AND"] = """\
LOD $op1
NND $op2
NOT ACC
STR $dest"""

binMac["OR"] = """\
NOT $op1 INTO macro[0]
LOD $op2
NOT ACC
NND macro[0]
STR $dest"""

binMac["NOR"] = """\
NOT $op1 INTO macro[0]
LOD $op2
NOT ACC
NND macro[0]
NOT ACC
STR $dest"""

binMac["XOR"] = """\
LOD $op1
NND $op2
STR macro[0]
NND $op1
STR macro[1]
LOD macro[0]
NND $op2
NND macro[1]
STR $dest"""

binMac["XNOR"] = """\
LOD $op1
NND $op2
STR macro[0]
NND $op1
STR macro[1]
LOD macro[0]
NND $op2
NND macro[1]
NOT ACC
STR $dest"""


#larger binary operation macros

binMac["ADD8"] = """\
ADD $op1[1] $op2[1] INTO $dest[1]
GETCARR ACC
ADDC $op1[0] $op2[0] INTO $dest[0]"""

binMac["ADD16"] = """\
ADD8 $op1[3] $op2[3] INTO $dest[3]
ADDC $op1[1] $op2[1] INTO $dest[1]
ADDC $op1[0] $op2[0] INTO $dest[0]"""

binMac["ADD32"] = """\
ADD16 $op1[7] $op2[7] INTO $dest[7]
ADDC $op1[3] $op2[3] INTO $dest[3]
ADDC $op1[2] $op2[2] INTO $dest[2]
ADDC $op1[1] $op2[1] INTO $dest[1]
ADDC $op1[0] $op2[0] INTO $dest[0]"""

binMac["ADD64"] = """\
ADD32 $op1[F] $op2[F] INTO $dest[F]
ADDC $op1[7] $op2[7] INTO $dest[7]
ADDC $op1[6] $op2[6] INTO $dest[6]
ADDC $op1[5] $op2[5] INTO $dest[5]
ADDC $op1[4] $op2[4] INTO $dest[4]
ADDC $op1[3] $op2[3] INTO $dest[3]
ADDC $op1[2] $op2[2] INTO $dest[2]
ADDC $op1[1] $op2[1] INTO $dest[1]
ADDC $op1[0] $op2[0] INTO $dest[0]"""

binMac["SUB8"] = """\
NOT8 $op2 INTO macro[3]
LOD N_[1]
ADDC $op1[1] macro[4] INTO $dest[1]
ADD $op1[0]
ADD macro[3]
STR $dest[0]"""

binMac["SUB16"] = """\
NOT16 $op2 INTO macro[3]
LOD N_[1]
ADDC $op1[3] macro[6] INTO $dest[3]
ADDC $op1[2] macro[5] INTO $dest[2]
ADDC $op1[1] macro[4] INTO $dest[1]
ADD $op1[0]
ADD macro[3]
STR $dest[0]"""

binMac["SUB32"] = """\
NOT32 $op2 INTO macro[3]
LOD N_[1]
ADDC $op1[7] macro[A] INTO $dest[7]
ADDC $op1[6] macro[9] INTO $dest[6]
ADDC $op1[5] macro[8] INTO $dest[5]
ADDC $op1[4] macro[7] INTO $dest[4]
ADDC $op1[3] macro[6] INTO $dest[3]
ADDC $op1[2] macro[5] INTO $dest[2]
ADDC $op1[1] macro[4] INTO $dest[1]
ADD $op1[0]
ADD macro[3]
STR $dest[0]"""

binMac["SUB64"] = """\
NOT64 $op2 INTO macro[3]
LOD N_[1]
ADDC $op1[F] macro[12] INTO $dest[F]
ADDC $op1[E] macro[11] INTO $dest[E]
ADDC $op1[D] macro[10] INTO $dest[D]
ADDC $op1[C] macro[F] INTO $dest[C]
ADDC $op1[B] macro[E] INTO $dest[B]
ADDC $op1[A] macro[D] INTO $dest[A]
ADDC $op1[9] macro[C] INTO $dest[9]
ADDC $op1[8] macro[B] INTO $dest[8]
ADDC $op1[7] macro[A] INTO $dest[7]
ADDC $op1[6] macro[9] INTO $dest[6]
ADDC $op1[5] macro[8] INTO $dest[5]
ADDC $op1[4] macro[7] INTO $dest[4]
ADDC $op1[3] macro[6] INTO $dest[3]
ADDC $op1[2] macro[5] INTO $dest[2]
ADDC $op1[1] macro[4] INTO $dest[1]
ADD $op1[0]
ADD macro[3]
STR $dest[0]"""

binMac["NAND8"] = """\
NAND $op1[0] $op2[0] INTO $dest[0]
NAND $op1[1] $op2[1] INTO $dest[1]"""

binMac["NAND16"] = """\
NAND8 $op1[0] $op2[0] INTO $dest[0]
NAND8 $op1[2] $op2[2] INTO $dest[2]"""

binMac["NAND32"] = """\
NAND16 $op1[0] $op2[0] INTO $dest[0]
NAND16 $op1[4] $op2[4] INTO $dest[4]"""

binMac["NAND64"] = """\
NAND32 $op1[0] $op2[0] INTO $dest[0]
NAND32 $op1[8] $op2[8] INTO $dest[8]"""

binMac["AND8"] = """\
AND $op1[0] $op2[0] INTO $dest[0]
AND $op1[1] $op2[1] INTO $dest[1]"""

binMac["AND16"] = """\
AND8 $op1[0] $op2[0] INTO $dest[0]
AND8 $op1[2] $op2[2] INTO $dest[2]"""

binMac["AND32"] = """\
AND16 $op1[0] $op2[0] INTO $dest[0]
AND16 $op1[4] $op2[4] INTO $dest[4]"""

binMac["AND64"] = """\
AND32 $op1[0] $op2[0] INTO $dest[0]
AND32 $op1[8] $op2[8] INTO $dest[8]"""

binMac["OR8"] = """\
OR $op1[0] $op2[0] INTO $dest[0]
OR $op1[1] $op2[1] INTO $dest[1]"""

binMac["OR16"] = """\
OR8 $op1[0] $op2[0] INTO $dest[0]
OR8 $op1[2] $op2[2] INTO $dest[2]"""

binMac["OR32"] = """\
OR16 $op1[0] $op2[0] INTO $dest[0]
OR16 $op1[4] $op2[4] INTO $dest[4]"""

binMac["OR64"] = """\
OR32 $op1[0] $op2[0] INTO $dest[0]
OR32 $op1[8] $op2[8] INTO $dest[8]"""

binMac["NOR8"] = """\
NOR $op1[0] $op2[0] INTO $dest[0]
NOR $op1[1] $op2[1] INTO $dest[1]"""

binMac["NOR16"] = """\
NOR8 $op1[0] $op2[0] INTO $dest[0]
NOR8 $op1[2] $op2[2] INTO $dest[2]"""

binMac["NOR32"] = """\
NOR16 $op1[0] $op2[0] INTO $dest[0]
NOR16 $op1[4] $op2[4] INTO $dest[4]"""

binMac["NOR64"] = """\
NOR32 $op1[0] $op2[0] INTO $dest[0]
NOR32 $op1[8] $op2[8] INTO $dest[8]"""

binMac["XOR8"] = """\
XOR $op1[0] $op2[0] INTO $dest[0]
XOR $op1[1] $op2[1] INTO $dest[1]"""

binMac["XOR16"] = """\
XOR8 $op1[0] $op2[0] INTO $dest[0]
XOR8 $op1[2] $op2[2] INTO $dest[2]"""

binMac["XOR32"] = """\
XOR16 $op1[0] $op2[0] INTO $dest[0]
XOR16 $op1[4] $op2[4] INTO $dest[4]"""

binMac["XOR64"] = """\
XOR32 $op1[0] $op2[0] INTO $dest[0]
XOR32 $op1[8] $op2[8] INTO $dest[8]"""

binMac["XNOR8"] = """\
XNOR $op1[0] $op2[0] INTO $dest[0]
XNOR $op1[1] $op2[1] INTO $dest[1]"""

binMac["XNOR16"] = """\
XNOR8 $op1[0] $op2[0] INTO $dest[0]
XNOR8 $op1[2] $op2[2] INTO $dest[2]"""

binMac["XNOR32"] = """\
XNOR16 $op1[0] $op2[0] INTO $dest[0]
XNOR16 $op1[4] $op2[4] INTO $dest[4]"""

binMac["XNOR64"] = """\
XNOR32 $op1[0] $op2[0] INTO $dest[0]
XNOR32 $op1[8] $op2[8] INTO $dest[8]"""

#jump macros, 4-bit
jmpMac = dict()

jmpMac["JMPEQ"] = """\
XOR $op1 $op2 INTO macro[0]
LOD macro[0]
JMP $dest"""

jmpMac["JMPNE"] = """\
XOR $op1 $op2 INTO macro[0]
LOGNOT ACC
JMP $dest"""

jmpMac["JMPG"] = """\
LOD $op1
NEG ACC
ADD $op2
GETCMP ACC
LOGNOT ACC
JMP $dest"""

jmpMac["JMPGE"] = """\
LOD $op2
NEG ACC
ADD $op1
GETCMP ACC
JMP $dest"""

jmpMac["JMPL"] = """\
LOD $op2
NEG ACC
ADD $op1
GETCMP ACC
LOGNOT ACC
JMP $dest"""

jmpMac["JMPLE"] = """\
LOD $op1
NEG ACC
ADD $op2
GETCMP ACC
JMP $dest"""



# I know it looks weird having the main function hide
# all the way down here, but it avoids the need to
# force the interpreter to load all the other stuff
# first. Besides, a good main function is usually
# pretty sparse.

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

if memUsed > 0:
	outFile.write(";memory space used by macros\n")
	outFile.write("macro: .data " + str(memUsed + 1) + "\n\n")

inFile.close()
outFile.close()
		

