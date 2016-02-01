#!/usr/bin/python


#Accumulator-based Macros
accMac = dict()

accMac["NOT"] = """\
NND N_[F]"""

accMac["NEG"] = """\
CLRCARR ACC
NOT ACC
ADD N_[1]"""

accMac["CLRCARR"] = """\
STR macro[0]
UCLC ACC
LOD macro[0]"""

accMac["SETCARR"] = """\
STR macro[0]
USTC ACC
LOD macro[0]"""

accMac["UCLC"] = """\
LOD N_[0]
ADD N_[0]"""

accMac["USTC"] = """\
LOD N_[8]
ADD N_[8]"""

accMac["GETCARR"] = """\
LOD N_[0]
ADD N_[0]"""

accMac["GETCMP"] = """\
CXA 0
NND N_[8]
NND N_[F]"""

accMac["INC"] = """\
CLRCARR ACC
ADD N_[1]"""

accMac["DEC"] = """\
CLRCARR ACC
ADD N_[F]"""

accMac["LSHIFT"] = """\
STR macro[0]
UCLC ACC
LOD macro[0]
ADD macro[0]"""

accMac["LROT"] = """\
STR macro[0]
UCLC ACC
LOD macro[0]
ADD macro[0]
ADD N_[0]"""

accMac["LOGNOT"] = """\
CLRCARR ACC
ADD N_[F]
CXA 0
NND N_[1]
NND N_[1]
NND N_[F]"""

accMac["SIGNEX"] = """\
CLRCARR ACC
ADD N_[8]
LOD N_[F]
ADD N_[0]
NND N_[F]"""

accMac["BEEP"] = """\
STR macro[0]
LOD N_[D]
STR 0
LOD N_[4]
STR 1
LOD macro[0]
STR 2
LOD N_[F]
STR 0
LOD N_[0]
STR 1
LOD macro[0]"""


