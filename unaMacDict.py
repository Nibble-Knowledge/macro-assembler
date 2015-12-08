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


