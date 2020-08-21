#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

# print8 = "examples/print8.ls8"
# mult = "examples/mult.ls8"
# stack = "examples/stack.ls8"
# call = "examples/call.ls8"
test = "sctest.ls8"

cpu = CPU()

cpu.load(test)
cpu.run()
