#!/usr/bin/python


#Note for future modifications: 2's complement compare flag
#(the XOR of the sign and overflow flags) being 1 means that
#the subtraction result was strictly less than zero


jmpMac = dict()

jmpMac["JMPEQ"] = """\
XOR $op1 $op2 INTO macro[2]
LOD macro[2]
JMP $dest"""

jmpMac["JMPNE"] = """\
XOR $op1 $op2 INTO macro[2]
LOD macro[2]
LOGNOT ACC
JMP $dest"""

#inverse of JMPLE
jmpMac["JMPG"] = """\
USTC ACC
CMPC $op1 $op2
GETCMP ACC
LOGNOT ACC
JMP $dest"""

#inverse of JMPGE
jmpMac["JMPL"] = """\
USTC ACC
CMPC $op2 $op1
GETCMP ACC
LOGNOT ACC
JMP $dest"""

#Subtract op1 from op2
#if CMP is 0, result was 0 or greater
#thus op1 was GE to op2
jmpMac["JMPGE"] = """\
USTC ACC
CMPC $op2 $op1
GETCMP ACC
JMP $dest"""

#subtract op2 from op1
#if CMP is 0, result was 0 or greater
#so thus op2 was less than or equal to op1
jmpMac["JMPLE"] = """\
USTC ACC
CMPC $op1 $op2
GETCMP ACC
JMP $dest"""

#larger jump macros.

jmpMac["JMPEQ8"] = """\
XOR8 $op1 $op2 INTO macro[2]
OR macro[2] macro[3] INTO macro[1]
LOD macro[1]
JMP $dest"""

jmpMac["JMPNE8"] = """\
XOR8 $op1 $op2 INTO macro[2]
OR macro[3] macro[2] INTO macro[1]
LOD macro[1]
LOGNOT ACC
JMP $dest"""

jmpMac["JMPEQ16"] = """\
XOR16 $op1 $op2 INTO macro[2]
OR macro[2] macro[5] INTO macro[2]
OR macro[2] macro[4] INTO macro[2]
OR macro[2] macro[3] INTO macro[2]
LOD macro[2]
JMP $dest"""

jmpMac["JMPNE16"] = """\
XOR16 $op1 $op2 INTO macro[2]
OR macro[2] macro[5] INTO macro[2]
OR macro[2] macro[4] INTO macro[2]
OR macro[2] macro[3] INTO macro[2]
LOD macro[2]
LOGNOT ACC
JMP $dest"""

jmpMac["JMPEQ32"] = """\
XOR32 $op1 $op2 INTO macro[2]
OR macro[2] macro[9] INTO macro[2]
OR macro[2] macro[8] INTO macro[2]
OR macro[2] macro[7] INTO macro[2]
OR macro[2] macro[6] INTO macro[2]
OR macro[2] macro[5] INTO macro[2]
OR macro[2] macro[4] INTO macro[2]
OR macro[2] macro[3] INTO macro[2]
LOD macro[2]
JMP $dest"""

jmpMac["JMPNE32"] = """\
XOR32 $op1 $op2 INTO macro[2]
OR macro[2] macro[9] INTO macro[2]
OR macro[2] macro[8] INTO macro[2]
OR macro[2] macro[7] INTO macro[2]
OR macro[2] macro[6] INTO macro[2]
OR macro[2] macro[5] INTO macro[2]
OR macro[2] macro[4] INTO macro[2]
OR macro[2] macro[3] INTO macro[2]
LOD macro[2]
LOGNOT ACC
JMP $dest"""

jmpMac["JMPEQ64"] = """\
XOR64 $op1 $op2 INTO macro[2]
OR macro[2] macro[11] INTO macro[2]
OR macro[2] macro[10] INTO macro[2]
OR macro[2] macro[F] INTO macro[2]
OR macro[2] macro[E] INTO macro[2]
OR macro[2] macro[D] INTO macro[2]
OR macro[2] macro[C] INTO macro[2]
OR macro[2] macro[B] INTO macro[2]
OR macro[2] macro[A] INTO macro[2]
OR macro[2] macro[9] INTO macro[2]
OR macro[2] macro[8] INTO macro[2]
OR macro[2] macro[7] INTO macro[2]
OR macro[2] macro[6] INTO macro[2]
OR macro[2] macro[5] INTO macro[2]
OR macro[2] macro[4] INTO macro[2]
OR macro[2] macro[3] INTO macro[2]
LOD macro[2]
JMP $dest"""

jmpMac["JMPNE64"] = """\
XOR64 $op1 $op2 INTO macro[2]
OR macro[2] macro[11] INTO macro[2]
OR macro[2] macro[10] INTO macro[2]
OR macro[2] macro[F] INTO macro[2]
OR macro[2] macro[E] INTO macro[2]
OR macro[2] macro[D] INTO macro[2]
OR macro[2] macro[C] INTO macro[2]
OR macro[2] macro[B] INTO macro[2]
OR macro[2] macro[A] INTO macro[2]
OR macro[2] macro[9] INTO macro[2]
OR macro[2] macro[8] INTO macro[2]
OR macro[2] macro[7] INTO macro[2]
OR macro[2] macro[6] INTO macro[2]
OR macro[2] macro[5] INTO macro[2]
OR macro[2] macro[4] INTO macro[2]
OR macro[2] macro[3] INTO macro[2]
LOD macro[2]
LOGNOT ACC
JMP $dest"""

jmpMac["JMPG8"] = """\
USTC ACC
CMPC $op1[1] $op2[1]
CMPC $op1[0] $op2[0]
GETCMP ACC
LOGNOT ACC
JMP $dest"""

jmpMac["JMPL8"] = """\
JMPG8 $op2 $op1 $dest
"""

jmpMac["JMPLE8"] = """\
USTC ACC
CMPC $op1[1] $op2[1]
CMPC $op1[0] $op2[0]
GETCMP ACC
JMP $dest"""

jmpMac["JMPGE8"] = """\
JMPLE8 $op2 $op1 TO $dest"""

jmpMac["JMPG16"] = """\
USTC ACC
CMPC $op1[3] $op2[3]
CMPC $op1[2] $op2[2]
CMPC $op1[1] $op2[1]
CMPC $op1[0] $op2[0]
GETCMP ACC
LOGNOT ACC
JMP $dest
"""

jmpMac["JMPL16"] = """\
JMPG16 $op2 $op1 $dest
"""

jmpMac["JMPLE16"] = """\
USTC ACC
CMPC $op1[3] $op2[3]
CMPC $op1[2] $op2[2]
CMPC $op1[1] $op2[1]
CMPC $op1[0] $op2[0]
GETCMP ACC
JMP $dest"""

jmpMac["JMPGE16"] = """\
JMPL16 $op2 $op1 TO $dest"""

jmpMac["JMPL32"] = """\
JMPG32 $op2 $op1 TO $dest"""

jmpMac["JMPG32"] = """\
USTC ACC
CMPC $op1[7] $op2[7]
CMPC $op1[6] $op2[6]
CMPC $op1[5] $op2[5]
CMPC $op1[4] $op2[4]
CMPC $op1[3] $op2[3]
CMPC $op1[2] $op2[2]
CMPC $op1[1] $op2[1]
CMPC $op1[0] $op2[0]
GETCMP ACC
LOGNOT ACC
JMP $dest
"""

jmpMac["JMPLE32"] = """\
USTC ACC
CMPC $op1[7] $op2[7]
CMPC $op1[6] $op2[6]
CMPC $op1[5] $op2[5]
CMPC $op1[4] $op2[4]
CMPC $op1[3] $op2[3]
CMPC $op1[2] $op2[2]
CMPC $op1[1] $op2[1]
CMPC $op1[0] $op2[0]
GETCMP ACC
JMP $dest"""

jmpMac["JMPGE32"] = """\
JMPLE32 $op2 $op1 TO $dest"""

jmpMac["JMPL64"] = """\
JMPG64 $op2 $op1 TO $dest"""

jmpMac["JMPG64"] = """\
USTC ACC
CMPC $op1[F] $op2[F]
CMPC $op1[E] $op2[E]
CMPC $op1[D] $op2[D]
CMPC $op1[C] $op2[C]
CMPC $op1[B] $op2[B]
CMPC $op1[A] $op2[A]
CMPC $op1[9] $op2[9]
CMPC $op1[8] $op2[8]
CMPC $op1[7] $op2[7]
CMPC $op1[6] $op2[6]
CMPC $op1[5] $op2[5]
CMPC $op1[4] $op2[4]
CMPC $op1[3] $op2[3]
CMPC $op1[2] $op2[2]
CMPC $op1[1] $op2[1]
CMPC $op1[0] $op2[0]
GETCMP ACC
LOGNOT ACC
JMP $dest"""


jmpMac["JMPLE64"] = """\
USTC ACC
CMPC $op1[F] $op2[F]
CMPC $op1[E] $op2[E]
CMPC $op1[D] $op2[D]
CMPC $op1[C] $op2[C]
CMPC $op1[B] $op2[B]
CMPC $op1[A] $op2[A]
CMPC $op1[9] $op2[9]
CMPC $op1[8] $op2[8]
CMPC $op1[7] $op2[7]
CMPC $op1[6] $op2[6]
CMPC $op1[5] $op2[5]
CMPC $op1[4] $op2[4]
CMPC $op1[3] $op2[3]
CMPC $op1[2] $op2[2]
CMPC $op1[1] $op2[1]
CMPC $op1[0] $op2[0]
GETCMP ACC
JMP $dest"""

jmpMac["JMPGE64"] = """\
JMPLE64 $op2 $op1 TO $dest"""

