#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author:left_left
import binascii
import re

def jpg2bin(data):
    b64 = binascii.b2a_base64(data)
    j = 0
    
    f = open('test.txt', 'w')
    for i in b64:
        f.write("".join([bin(int(binascii.b2a_hex(i), 16))[2:].rjust(8,'0'), " "]))
        j += 1
        if j % 6 == 0:
            f.write('\n')
    f.close()
    print "jpg to bin ok"

def bin2jpg(data):
    result = re.split(r'[ \n]', data)
    b64 =  ""
    for i in result:  
        if i:
            hex_src = str(hex(int(i, 2)))[2:].rjust(2,"0")
            b64 = "".join([b64, binascii.a2b_hex(hex_src)])
            
    bin_data = binascii.a2b_base64(b64)
    f = open("new.jpg", 'wb')
    f.write(bin_data)
    f.close()
    print "jpg to bin ok"
    
def main():
    f = open("test.jpg", "rb")
    data = f.read()
    jpg2bin(data)
    f.close()

    f = open("test.txt")
    data = f.read()
    bin2jpg(data)
    f.close()

if __name__ == "__main__":
    main()