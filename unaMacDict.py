#!/usr/bin/python


unaMac = dict()

unaMac["MOV"] = """\
LOD $op1[0]
STR $dest[0]"""

unaMac["NOT"] = """\
LOD $op1
NOT ACC
STR $dest"""

unaMac["NEG"] = """\
UCLC ACC
LOD $op1
NOT ACC
ADD N_[1]
STR $dest"""

unaMac["PROPCARR"] = """\
LOD N_[0]
ADD $op1
STR $dest"""

unaMac["PROPNEG"] = """\
LOD $op1[0]
NND N_[F]
ADD N_[0]
STR $dest[0]"""

unaMac["INC"] = """\
UCLC ACC
LOD N_[1]
ADD $op1
STR $dest"""

unaMac["LSHIFT"] = """\
UCLC ACC
LOD N_[0]
ADD $op1
ADD $op1
STR $dest"""

unaMac["LROT"] = """\
UCLC ACC
LOD $op1
ADD $op1
ADD N_[0]
STR $dest"""

unaMac["MOVADDR"] = """\
LOD &op1[0]
STR $dest[0]
LOD &op1[1]
STR $dest[1]
LOD &op1[2]
STR $dest[2]
LOD &op1[3]
STR $dest[3]"""

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
NEG $op1[1] INTO $dest[1]
PROPNEG $op1[0] INTO $dest[0]"""

unaMac["NEG16"] = """\
NEG8 $op1[2] INTO $dest[2]
PROPNEG $op1[1] INTO $dest[1]
PROPNEG $op1[0] INTO $dest[0]"""

unaMac["NEG32"] = """\
NEG16 $op1[4] INTO $dest[4]
PROPNEG $op1[3] INTO $dest[3]
PROPNEG $op1[2] INTO $dest[2]
PROPNEG $op1[1] INTO $dest[1]
PROPNEG $op1[0] INTO $dest[0]"""

unaMac["NEG64"] = """\
NEG32 $op1[8] INTO $dest[8]
PROPNEG $op1[7] INTO $dest[7]
PROPNEG $op1[6] INTO $dest[6]
PROPNEG $op1[5] INTO $dest[5]
PROPNEG $op1[4] INTO $dest[4]
PROPNEG $op1[3] INTO $dest[3]
PROPNEG $op1[2] INTO $dest[2]
PROPNEG $op1[1] INTO $dest[1]
PROPNEG $op1[0] INTO $dest[0]"""

unaMac["INC8"] = """\
USTC ACC
PROPCARR $op1[1] INTO $dest[1]
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
LOD N_[0]
ADD $dest[1]
STR $dest[1]"""

unaMac["LROT16"] = """\
LSHIFT16 $op1 INTO $dest
LOD N_[0]
ADD $dest[3]
STR $dest[3]"""

unaMac["LROT32"] = """\
LSHIFT32 $op1 INTO $dest
LOD N_[0]
ADD $dest[7]
STR $dest[7]"""

unaMac["LROT64"] = """\
LSHIFT64 $op1 INTO $dest
LOD N_[0]
ADD $dest[F]
STR $dest[F]"""


