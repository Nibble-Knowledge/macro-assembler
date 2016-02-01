#!/usr/bin/python


binMac = dict()

binMac["ADD"] = """\
UCLC ACC
ADDC $op1 $op2 INTO $dest"""

binMac["ADDC"] = """\
LOD $op1
ADD $op2
STR $dest"""

binMac["SUB"] = """\
USTC ACC
SUBC $op1 $op1 INTO $dest"""

binMac["SUBC"] = """\
LOD $op2
NOT ACC
ADD $op1
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
ADDC $op1[0] $op2[0] INTO $dest[0]"""

binMac["ADD16"] = """\
ADD8 $op1[2] $op2[2] INTO $dest[2]
ADDC $op1[1] $op2[1] INTO $dest[1]
ADDC $op1[0] $op2[0] INTO $dest[0]"""

binMac["ADD32"] = """\
ADD16 $op1[4] $op2[4] INTO $dest[4]
ADDC $op1[3] $op2[3] INTO $dest[3]
ADDC $op1[2] $op2[2] INTO $dest[2]
ADDC $op1[1] $op2[1] INTO $dest[1]
ADDC $op1[0] $op2[0] INTO $dest[0]"""

binMac["ADD64"] = """\
ADD32 $op1[8] $op2[8] INTO $dest[8]
ADDC $op1[7] $op2[7] INTO $dest[7]
ADDC $op1[6] $op2[6] INTO $dest[6]
ADDC $op1[5] $op2[5] INTO $dest[5]
ADDC $op1[4] $op2[4] INTO $dest[4]
ADDC $op1[3] $op2[3] INTO $dest[3]
ADDC $op1[2] $op2[2] INTO $dest[2]
ADDC $op1[1] $op2[1] INTO $dest[1]
ADDC $op1[0] $op2[0] INTO $dest[0]"""

binMac["SUB8"] = """\
SUB $op1[1] $op2[1] INTO $dest[1]
SUBC $op1 $op2 INTO $dest"""

binMac["SUB16"] = """\
SUB8 $op1[2] $op2[2] INTO $dest[2]
SUBC $op1[1] $op2[1] INTO $dest[1]
SUBC $op1[0] $op2[0] INTO $dest[0]"""

binMac["SUB32"] = """\
SUB16 $op1[4] $op2[4] INTO $dest[4]
SUBC $op1[3] $op2[3] INTO $dest[3]
SUBC $op1[2] $op2[2] INTO $dest[2]
SUBC $op1[1] $op2[1] INTO $dest[1]
SUBC $op1[0] $op2[0] INTO $dest[0]"""

binMac["SUB64"] = """\
SUB32 $op1[8] $op2[8] INTO $dest[8]
SUBC $op1[7] $op2[7] INTO $dest[7]
SUBC $op1[6] $op2[6] INTO $dest[6]
SUBC $op1[5] $op2[5] INTO $dest[5]
SUBC $op1[4] $op2[4] INTO $dest[4]
SUBC $op1[3] $op2[3] INTO $dest[3]
SUBC $op1[2] $op2[2] INTO $dest[2]
SUBC $op1[1] $op2[1] INTO $dest[1]
SUBC $op1[0] $op2[0] INTO $dest[0]"""

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


