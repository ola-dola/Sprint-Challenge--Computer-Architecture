#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) != 2:
    raise Exception("You have to pass in the file to read/write")

# assert(len(sys.argv) == 2), "You have to pass in a filename to read/write"

# if len(sys.argv) != 2:
#     print(f"usage: {sys.argv[0]} <filename>")
#     sys.exit(1)

cpu = CPU()

cpu.load(sys.argv[1])
cpu.run()
