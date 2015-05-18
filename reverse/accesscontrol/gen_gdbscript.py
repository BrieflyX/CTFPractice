#!/usr/bin/env python
# coding: utf-8

import sys
if len(sys.argv) < 3:
    print 'Usage: %s addr string' % sys.argv[0]

addr = int(sys.argv[1][2:], 16)
string = sys.argv[2]

for ch in string:
    print 'set {char}0x%x=%d' % (addr, ord(ch))
    addr += 1
print 'set {char}0x%x=0' % addr

