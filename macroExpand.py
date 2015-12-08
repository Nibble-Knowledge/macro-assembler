#!/usr/bin/python

# Naomi Hiebert coded this



#import our data structures
from accMacDict import accMac
from unaMacDict import unaMac
from binMacDict import binMac
from jmpMacDict import jmpMac
from asmDicts import opcodes, unaryOpcodes, dataTypes

#import global variables
import globalVars

#hardcoded lists - for identifying macro types




# The real heart of the operation - identifies macros anywhere,
# including inside other macros! Tends to get called recursively
# since macros inside macros need to be expanded inside macros.

#Takes: a split line
#Returns: a list of (joined) lines

def expandline(splitline):
	expLine = []

	if isFallthroughLine(splitline): #the base case - encompasses several other cases
		expLine.append(" ".join(splitline))

	elif isINFLine(splitline):
		getINFValue(splitline)

	elif isIncludeStatement(splitline):
		expLine.append(handleInclude(splitline))

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
	else:
		return False

#INF header lines get grabbed
def isINFLine(splitline):
	if len(splitline) == 2 and splitline[0] == "INF":
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
		if globalVars.DataFields:
			structurefail(splitline)
		return True
	elif len(splitline) == 1 and splitline[0] in unaryOpcodes:
		if globalVars.DataFields:
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


#checks if it's a data declaration, possibly with label
def isData(splitline):
	if len(splitline) > 1 and splitline[0] in dataTypes:
		globalVars.DataFields = True
		return True
	elif len(splitline) > 2 and splitline[1] in dataTypes:
		globalVars.DataFields = True
		return True
	else:
		return False

#detects INCL statements
def isIncludeStatement(splitline):
	if splitline[0] == "INCL" and len(splitline) == 2:
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

#complains when you ask for the fifth or greater nibble of an address
def addroffsetfail(errortoken):
	raise Exception("Addressing Error: Addresses are only four nibbles long!", errortoken)


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
		splitline = replaceLabels(splitline, "&op1", op1)
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
#		the placeholder (starts with $ or maybe &) label to replace
#		the new label (maybe with [offset]) to replace it with
#Also note that the placeholder in the line may also have an offset
#Returns: a split line
#Edits: global "memUsed" variable, if necessary
def replaceLabels(splitline, oldlabel, replabel):
	outline = []

	for token in splitline:
		#put it in the output line, adapted
		if token.startswith(oldlabel) and "$" in oldlabel:
			outline.append(reptoken(token, replabel))
		elif token.startswith(oldlabel) and "&" in oldlabel:
			outline.append(repaddress(token, replabel))
		else:
			#not the label we're looking for
			outline.append(token)

		#check if we're using macro memory. If so, we might need to 
		#expand our macro memory bank.
		if "macro[" in outline[-1]:
			macoffset = outline[-1][outline[-1].index('[') + 1 : outline[-1].index(']')]
			macoffset = int(macoffset, 16)
			if macoffset > globalVars.memUsed:
				globalVars.memUsed = macoffset

	return outline

#Takes:	The token to replace (maybe with offset, starts with $)
#		The new label to replace things with
#Returns:
#		A new token, with calculate labels
#Assumes:
#		If replabel or token uses the "&" syntax, it already has
#		the trailing [] present, as &(label[A])[B] but definitely
#		not &(label[A]). This is always the case if this program
#		applied the "&" syntax itself; users might break things.
def reptoken(token, replabel):
	#default values, if no offset found
	oldoffset = 0
	repoffset = 0

	#get the offset from the replacement, if necessary
	if '[' in replabel and ']' in replabel:
		repoffset = replabel[replabel.rindex('[') + 1 : replabel.rindex(']')]
		repoffset = hexSmartInt(repoffset)

	#and from the old label, if necessary
	if '[' in token and ']' in token:
		oldoffset = token[token.rindex('[') + 1 : token.rindex(']')]
		oldoffset = hexSmartInt(oldoffset)
			
	#add them together
	newoffset = oldoffset + repoffset

	#smash together the new token
	if '[' in replabel:
		newtoken = replabel[:replabel.rfind('[')] + '[' + hex(newoffset)[2:] + ']'
	else:
		newtoken = replabel + '[' + hex(newoffset)[2:] + ']'

	if '&' in newtoken and newoffset > 3:
		addroffsetfail(newtoken)
		
	return newtoken

#Takes: 	A token to replace (maybe with offset in [0:4], starts with &)
#			A label to replace it with (completely unrelated offset, not already using &)
#Returns:	A token formed as &(replabel[repoffset])[tokenoffset]
def repaddress(token, replabel):
	repoffset = 0
	addroffset = 0

	#get the offset from the replacement, if necessary
	if '[' in replabel and ']' in replabel:
		repoffset = replabel[replabel.index('[') + 1 : replabel.index(']')]
		repoffset = int(repoffset, 16)
		replabel = replabel[:replabel.find('[')]

	#and from the old label, if necessary
	if '[' in token and ']' in token:
		addroffset = token[token.index('[') + 1 : token.index(']')]
		addroffset = int(addroffset, 16)
		token = token[:token.find('[')]

	#assemble new token
	newtoken = "&(" + replabel + '[' + hex(repoffset)[2:] + "])[" + hex(addroffset)[2:] + ']'
	return newtoken


#deal with include statements by adding them to the FList queue
def handleInclude(splitline):
	if splitline[1] not in globalVars.FList:
		globalVars.FList.append(splitline[1])
		return ";Included " + splitline[1]
	else:
		return ";Ignored repeated include: " + splitline[1]

#deal with INF statements by, if they're in the first file,
#setting out output INF statement to have the given value.
#If there's no statement in the first file, use the default
#(1024).
def getINFValue(splitline):
	if globalVars.FIndex != 0:
		return
	else:
		globalVars.BAddr = int(splitline[1], 0)


#Like int(token, 0) but defaults to hexadecimal.
def hexSmartInt(token):
	if token[0] == '0' and not token.isdigit():
		if len(token) > 2 and token[1] == 'd':
			return int(token[2:], 10)
		else:
			return int(token, 0)
	else:
		return int(token, 16)

