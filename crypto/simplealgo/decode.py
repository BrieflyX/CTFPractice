#!/usr/bin/python
# coding: utf-8

def FAN(n, m=3):
    i = 0
    z = []
    s = 0
    while n > 0:
        if n % 2 != 0:
            z.append(2 - (n % 4))
        else:
            z.append(0)
        n = (n - z[i])/2
        i = i + 1
    z = z[::-1]
    l = len(z)
    for i in range(0, l):
        s += z[i] * m ** (l - 1 - i)
    return s

cipher = '2712733801194381163880124319146586498182192151917719248224681364019142438188097307292437016388011943193619457377217328473027324319178428'
iflag = 41420276958143763286534983262388590617348245863283796564325543769593976761661865423288189
table = {}

def generate_table():
    global table
    for i in range(100):
        cipher = FAN(i)
        table[str(cipher)] = '%02d' % i

def solve(s):
    result = []

    # the segment mustn't start with 0
    if s == '':
        return ['']
    if s[0] == '0':
        return []

    for i in range(4,0,-1):
        if s[:i] in table:
            sub_result = solve(s[i:])
            for sub in sub_result:
                result.append(table[s[:i]]+sub)
            break

    return result

generate_table()
print solve('2712733801194381163880124319146586498182192151917719248224681364019142438188097307292437016388011943193619457377217328473027324319178428')
# should know the last digit can be only one bit
# don't need the first character because it must be A ~ haha !
print hex(iflag)[2:-1].decode('hex')

