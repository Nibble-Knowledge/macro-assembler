#!/usr/bin/python


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

accMac["SIGNEX"] = """\
ADD N_[8]
CXA 0
NND N_[1]
ADD N_[1]"""

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


