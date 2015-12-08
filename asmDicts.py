#!/usr/bin/python	


	#native NK opcodes so we can identify them
opcodes = ["ADD", "NND", "LOD", "STR", "HLT", "CXA", "NOP", "JMP"]
unaryOpcodes = ["NOP", "CXA", "HLT"]

	#assembler-supported data type labels
dataTypes = [".data", ".ascii", ".asciiz"]
