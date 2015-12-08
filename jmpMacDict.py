#!/usr/bin/python


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

jmpMac["JMPG"] = """\
LOD $op1
NEG ACC
ADD $op2
GETCMP ACC
LOGNOT ACC
JMP $dest"""

jmpMac["JMPL"] = """\
LOD $op1
NEG ACC
ADD $op2
GETCMP ACC
JMP $dest"""

jmpMac["JMPGE"] = """\
JMPL $op2 $op1 TO $dest"""

jmpMac["JMPLE"] = """\
JMPG $op2 $op1 TO $dest"""

#larger jump macros.

jmpMac["JMPEQ8"] = """\
XOR8 $op1 $op2 INTO macro[2]
OR macro[2] macro[3] INTO macro[1]
LOD macro[1]
JMP $dest"""

jmpMac["JMPNE8"] = """\
XOR8 $op1 $op2 INTO macro[2]
OR macro[2] macro[3] INTO macro[1]
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
NOT8 $op1 INTO macro[4]
LOD N_[1]
ADD macro[5]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[1]
CXA
NND N_[1]
NND macro[0]
;Start dealing with the most significant nibble
ADD macro[4]
STR macro[2]
;1st partial sum in macro[2]
CXA
XOR macro[3] macro[2] INTO macro[3]
LOD macro[3]
STR macro[3]
;OVF1 in MSB of macro[3]
;get final CMP bit
LOD macro[2]
ADD $op2[0]
CXA
STR macro[2]
XOR macro[2] macro[3] INTO macro[3]
LOD macro[3]
NND N_[8]
NND N_[F]
LOGNOT ACC
JMP $dest
"""

jmpMac["JMPL8"] = """\
NOT8 $op1 INTO macro[4]
LOD N_[1]
ADD macro[5]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[1]
CXA
NND N_[1]
NND macro[0]
;Start dealing with the most significant nibble
ADD macro[4]
STR macro[2]
;1st partial sum in macro[2]
CXA
XOR macro[3] macro[2] INTO macro[3]
LOD macro[3]
STR macro[3]
;OVF1 in MSB of macro[3]
;get final CMP bit
LOD macro[2]
ADD $op2[0]
CXA
STR macro[2]
XOR macro[2] macro[3] INTO macro[3]
LOD macro[3]
NND N_[8]
NND N_[F]
JMP $dest
"""

jmpMac["JMPLE8"] = """\
JMPG8 $op2 $op1 TO $dest"""

jmpMac["JMPGE8"] = """\
JMPL8 $op2 $op1 TO $dest"""

jmpMac["JMPG16"] = """\
NOT16 $op1 INTO macro[4]
LOD N_[1]
ADD macro[7]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[3]
CXA
NND N_[1]
NND macro[0]
ADD macro[6]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[2]
CXA
NND N_[1]
NND macro[0]
ADD macro[5]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[1]
CXA
NND N_[1]
NND macro[0]
;Start dealing with the most significant nibble
ADD macro[4]
STR macro[2]
;1st partial sum in macro[2]
CXA
XOR macro[3] macro[2] INTO macro[3]
LOD macro[3]
STR macro[3]
;OVF1 in MSB of macro[3]
;get final CMP bit
LOD macro[2]
ADD $op2[0]
CXA
STR macro[2]
XOR macro[2] macro[3] INTO macro[3]
LOD macro[3]
NND N_[8]
NND N_[F]
LOGNOT ACC
JMP $dest
"""

jmpMac["JMPL16"] = """\
NOT16 $op1 INTO macro[4]
LOD N_[1]
ADD macro[7]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[3]
CXA
NND N_[1]
NND macro[0]
ADD macro[6]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[2]
CXA
NND N_[1]
NND macro[0]
ADD macro[5]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[1]
CXA
NND N_[1]
NND macro[0]
;Start dealing with the most significant nibble
ADD macro[4]
STR macro[2]
;1st partial sum in macro[2]
CXA
XOR macro[3] macro[2] INTO macro[3]
LOD macro[3]
STR macro[3]
;OVF1 in MSB of macro[3]
;get final CMP bit
LOD macro[2]
ADD $op2[0]
CXA
STR macro[2]
XOR macro[2] macro[3] INTO macro[3]
LOD macro[3]
NND N_[8]
NND N_[F]
JMP $dest
"""

jmpMac["JMPLE16"] = """\
JMPG16 $op2 $op1 TO $dest"""

jmpMac["JMPGE16"] = """\
JMPL16 $op2 $op1 TO $dest"""

jmpMac["JMPL32"] = """\
NOT32 $op1 INTO macro[4]
LOD N_[1]
ADD macro[B]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[7]
CXA
NND N_[1]
NND macro[0]
ADD macro[A]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[6]
CXA
NND N_[1]
NND macro[0]
ADD macro[9]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[5]
CXA
NND N_[1]
NND macro[0]
ADD macro[8]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[4]
CXA
NND N_[1]
NND macro[0]
ADD macro[7]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[3]
CXA
NND N_[1]
NND macro[0]
ADD macro[6]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[2]
CXA
NND N_[1]
NND macro[0]
ADD macro[5]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[1]
CXA
NND N_[1]
NND macro[0]
;Start dealing with the most significant nibble
ADD macro[4]
STR macro[2]
;1st partial sum in macro[2]
CXA
XOR macro[3] macro[2] INTO macro[3]
LOD macro[3]
STR macro[3]
;OVF1 in MSB of macro[3]
;get final CMP bit
LOD macro[2]
ADD $op2[0]
CXA
STR macro[2]
XOR macro[2] macro[3] INTO macro[3]
LOD macro[3]
NND N_[8]
NND N_[F]
JMP $dest
"""

jmpMac["JMPG32"] = """\
NOT32 $op1 INTO macro[4]
LOD N_[1]
ADD macro[B]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[7]
CXA
NND N_[1]
NND macro[0]
ADD macro[A]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[6]
CXA
NND N_[1]
NND macro[0]
ADD macro[9]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[5]
CXA
NND N_[1]
NND macro[0]
ADD macro[8]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[4]
CXA
NND N_[1]
NND macro[0]
ADD macro[7]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[3]
CXA
NND N_[1]
NND macro[0]
ADD macro[6]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[2]
CXA
NND N_[1]
NND macro[0]
ADD macro[5]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[1]
CXA
NND N_[1]
NND macro[0]
;Start dealing with the most significant nibble
ADD macro[4]
STR macro[2]
;1st partial sum in macro[2]
CXA
XOR macro[3] macro[2] INTO macro[3]
LOD macro[3]
STR macro[3]
;OVF1 in MSB of macro[3]
;get final CMP bit
LOD macro[2]
ADD $op2[0]
CXA
STR macro[2]
XOR macro[2] macro[3] INTO macro[3]
LOD macro[3]
NND N_[8]
NND N_[F]
LOGNOT ACC
JMP $dest
"""

jmpMac["JMPLE32"] = """\
JMPG32 $op2 $op1 TO $dest"""

jmpMac["JMPGE32"] = """\
JMPL32 $op2 $op1 TO $dest"""

jmpMac["JMPL64"] = """\
NOT64 $op1 INTO macro[4]
LOD N_[1]
ADD macro[13]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[F]
CXA
NND N_[1]
ADD macro[12]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[E]
CXA
NND N_[1]
ADD macro[11]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[D]
CXA
NND N_[1]
ADD macro[10]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[C]
CXA
NND N_[1]
ADD macro[F]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[B]
CXA
NND N_[1]
ADD macro[E]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[A]
CXA
NND N_[1]
ADD macro[D]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[9]
CXA
NND N_[1]
ADD macro[C]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[8]
CXA
NND N_[1]
ADD macro[B]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[7]
CXA
NND N_[1]
NND macro[0]
ADD macro[A]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[6]
CXA
NND N_[1]
NND macro[0]
ADD macro[9]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[5]
CXA
NND N_[1]
NND macro[0]
ADD macro[8]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[4]
CXA
NND N_[1]
NND macro[0]
ADD macro[7]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[3]
CXA
NND N_[1]
NND macro[0]
ADD macro[6]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[2]
CXA
NND N_[1]
NND macro[0]
ADD macro[5]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[1]
CXA
NND N_[1]
NND macro[0]
;Start dealing with the most significant nibble
ADD macro[4]
STR macro[2]
;1st partial sum in macro[2]
CXA
XOR macro[3] macro[2] INTO macro[3]
LOD macro[3]
STR macro[3]
;OVF1 in MSB of macro[3]
;get final CMP bit
LOD macro[2]
ADD $op2[0]
CXA
STR macro[2]
XOR macro[2] macro[3] INTO macro[3]
LOD macro[3]
NND N_[8]
NND N_[F]
JMP $dest
"""

jmpMac["JMPG64"] = """\
NOT64 $op1 INTO macro[4]
LOD N_[1]
ADD macro[13]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[F]
CXA
NND N_[1]
ADD macro[12]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[E]
CXA
NND N_[1]
ADD macro[11]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[D]
CXA
NND N_[1]
ADD macro[10]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[C]
CXA
NND N_[1]
ADD macro[F]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[B]
CXA
NND N_[1]
ADD macro[E]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[A]
CXA
NND N_[1]
ADD macro[D]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[9]
CXA
NND N_[1]
ADD macro[C]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[8]
CXA
NND N_[1]
ADD macro[B]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[7]
CXA
NND N_[1]
NND macro[0]
ADD macro[A]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[6]
CXA
NND N_[1]
NND macro[0]
ADD macro[9]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[5]
CXA
NND N_[1]
NND macro[0]
ADD macro[8]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[4]
CXA
NND N_[1]
NND macro[0]
ADD macro[7]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[3]
CXA
NND N_[1]
NND macro[0]
ADD macro[6]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[2]
CXA
NND N_[1]
NND macro[0]
ADD macro[5]
STR macro[1]
CXA
NND N_[1]
STR macro[0]
LOD macro[1]
ADD $op2[1]
CXA
NND N_[1]
NND macro[0]
;Start dealing with the most significant nibble
ADD macro[4]
STR macro[2]
;1st partial sum in macro[2]
CXA
XOR macro[3] macro[2] INTO macro[3]
LOD macro[3]
STR macro[3]
;OVF1 in MSB of macro[3]
;get final CMP bit
LOD macro[2]
ADD $op2[0]
CXA
STR macro[2]
XOR macro[2] macro[3] INTO macro[3]
LOD macro[3]
NND N_[8]
NND N_[F]
LOGNOT ACC
JMP $dest
"""


jmpMac["JMPLE64"] = """\
JMPG64 $op2 $op1 TO $dest"""

jmpMac["JMPGE64"] = """\
JMPL64 $op2 $op1 TO $dest"""

