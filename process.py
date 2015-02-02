import os
import binascii
from info import directory
from info import filename

os.chdir(directory)
lst = [] # raw list of bytes
atoms = [] # structured list of atoms
x = 0
state = 0
atom = {}
atomsize = 0
# state 0 is idle
# state 1 is reading atom size
# state 2 is reading atom type
# state 3 is reading decompression lib name
# state 4 is reading raw data

# if idle (0), then create a new list item (1)

with open(filename, "rb") as f:
    byte = f.read(1)
    while byte != "":# and x < 500:
        print "x: %s, State: %s" % (x, state)
        # Do stuff with byte.
        if state == 0:
            state = 1
            atom = {}
            #print "create new atom"
        elif state == 1:
            for i in range(4): # read three more bytes to finish the size
                #print i
                lst.append(byte)
                byte = f.read(1)
                x += 1
            atomsizehex = lst[x-4] + lst[x-3] + lst[x-2] + lst[x-1]
            atomsize = int(binascii.hexlify(atomsizehex),16)
            #print "atomsize: %s" % atomsize
            atom['atomsize'] = atomsize
            #print "size is %s %s %s %s" % (binascii.hexlify(lst[x-4]), binascii.hexlify(lst[x-3]), binascii.hexlify(lst[x-2]), binascii.hexlify(lst[x-1]))
            state = 2
        elif state == 2:
            for i in range(4): # read three more bytes to finish the type
                print i
                lst.append(byte)
                byte = f.read(1)
                x += 1
            atomtype = lst[x-4] + lst[x-3] + lst[x-2] + lst[x-1]
            #print atomtype
            atom['atomtype'] = atomtype
            #print "size is %s %s %s %s" % (binascii.hexlify(lst[x-4]), binascii.hexlify(lst[x-3]), binascii.hexlify(lst[x-2]), binascii.hexlify(lst[x-1]))
            if atomsize > 8:
                state = 3
            else:
                atoms.append(atom)
                #print atoms
                state = 0
        elif state == 3:
            for i in range(atomsize-8):
                #print i
                lst.append(byte)
                byte = f.read(1)
                x += 1
            rawdata = lst[x-atomsize+8]
            for i in range(x-atomsize+9, x):
                #print i
                rawdata += lst[i]
            
            #print "rawdata"
            #print rawdata
            
            #atom['rawdata'] = rawdata
            atoms.append(atom)
            
            #print atoms
            state = 0
print atoms
print x