#!/usr/bin/python


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


