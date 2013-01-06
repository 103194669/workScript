#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author:left_left
import sys
import os
import time
import select
import struct
import socket

'''
def chksum(packet):
    sum = 0
    i = 0
    p_len = len(packet)
    while i < p_len-1:
        sum = (ord(packet[i]) << 8) + ord(packet[i+1]) + sum
        i += 2
    if p_len & 1:
        sum += ord(packet[p_len-1])
    
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    sum = sum >> 8 | (sum << 8 & 0xffff)
    sum = sum ^ 0xffff
    return sum
'''

def data_format(seq, id):
    sum = id + seq + 8
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    sum = sum ^  0xffff
    '''
    header = struct.pack('bbHHh', 8, 0, 0, 
            id, seq)
    t = struct.pack('d', time.time())
    chk = chksum(header + t)
    '''
    header = struct.pack('bbHHh', 8, 0, sum,
            id, seq)
    return header

def time_format():
    if os.name == "nt":
        return time.clock()
    else:
        return time.time()

def recv_data(id, t, s):
    r, w, x = select.select([s], [], [], 1)
    if s in r:
        d = s.recvfrom(1024)
        p = d[0]
        if  not struct.unpack('H', p[24:26])[0] ^ id:
            t = time_format() - t
            print "%d bytes from %s: icmp_seq=%d ttl=%d time=%.3f ms" % (
                    len(p), d[1][0], struct.unpack('h', p[26:28])[0], int(ord(p[8])), t*1000)
            return 1
    else:
        print "Request timed out ..."
        return 0
        '''
        f = open('ping.ssp', 'wb')
        f.write(d[0])
        f.close()
        '''    
def ping(host):
    '''
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
    '''
    i = 0
    sent = 1
    suc_num = 1
    id = os.getpid()
    try:
        while 1:
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

            data = data_format(sent, id)
            t = time_format()
            s.sendto(data, (addr, 1))
            i = recv_data(id, t, s)
            suc_num += i
            sent += 1
            time.sleep(1)
    except KeyboardInterrupt:
        print "-------- %s ping statistics --------" % host
        print r"%d packets transmitted, %d received, %d%% packet loss" %(sent, 
                suc_num, (sent-suc_num) % sent * 100)

def main():
    try:
        host = sys.argv[1]
    except IndexError:
        print "Missing host ..."
        exit(1)

    result = ping(host)

if __name__ == '__main__':
    main()
