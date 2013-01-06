#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author:left_left
import sys
import os
import time
import struct
import socket

def data_format(seq):
    id = os.getpid()
    sum = id + seq + 8   
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    chk = sum ^  0xffff
    header = struct.pack('bbHHh', 8, 0, chk, 
            id, seq)
    
    return header

def ping(host):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, 1)
    except socket.error:
        print "Count connect %s" % host
        exit(1)
    try:
        addr = socket.gethostbyname(host)
        if not addr:
            raise 
    except:
        print "Please input the correct host ..."
        exit(1)

    i = 1
    try:
        while 1:
            data = data_format(i)
            t = time.time()
            s.sendto(data, (addr, 1))
            d = s.recvfrom(1024)
            t = time.time() - t
            
            print "%d bytes from %s: icmp_seq=%d ttl=%d time=%.3f ms" % (
                    len(d[0]), addr, i, int(ord(d[0][8])), t*1000)
            
            i += 1
            time.sleep(1)
    except KeyboardInterrupt:
        print "ping over."

def main():
    try:
        host = sys.argv[1]
    except IndexError:
        print "Missing host ..."
        exit(1)
    
    result = ping(host)

if __name__ == '__main__':
    main()
