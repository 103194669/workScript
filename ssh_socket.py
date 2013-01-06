#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author:left_left
import os
import sys
import struct
import select
import socket
import SocketServer
import paramiko
    
class Handler (SocketServer.StreamRequestHandler):
    def send_recv(self,chan):
        while True:
            r, w, x = select.select([self.request, chan], [], [])
            if self.request in r:
                data = self.request.recv(4096)
                if len(data) == 0:
                    break
                chan.send(data)
            if chan in r:
                data = chan.recv(4096)
                if len(data) == 0:
                    break
                self.request.send(data)
        chan.close()
        print 'Tunnel closed from %s:%s' % self.request.getpeername()
        self.request.close()
        
    def handle(self):
        print 'socks connection from %s:%s' % self.client_address    
        s = self.connection
        data = s.recv(1024)
        if ord(data[0]) == 4:
            self.chain_port = ord(data[3])
            self.chain_host = socket.inet_ntoa(data[4:8])
        else:
            s.send(b"\x05\x00")
            data = s.recv(1024)
            self.chain_host = socket.inet_ntoa(data[4:8])
            self.chain_port = ord(data[9])

        try:
            chan = self.ssh_transport.open_channel('direct-tcpip',
                                                   (self.chain_host, self.chain_port),
                                                   self.request.getpeername())
            local = self.client_address
            s.send("".join( [b"\x05\x00\x00\x01", socket.inet_aton(local[0]), struct.pack(">H", local[1])]))
        except Exception, e:
            print 'Incoming request to %s:%d failed: %s' % (self.chain_host, self.chain_port, repr(e))
            return
        if chan is None:
            print 'Incoming request to %s:%d was rejected by the SSH server.' % (self.chain_host, self.chain_port)
            return

        print 'Tunnel open from %s:%s' % self.request.getpeername()
                                                            
        self.send_recv(chan) 


def ssh_client(server='192.168.1.1', port=22, user='root', password='password'):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(server, port, user, password)
    except Exception, e:
        print "Error: %s" % e
        sys.exit(1)
    
    return client

def main():
    local_port = 10800
    password='zzzzzzz'
    server='172.18.0.210'
    client = ssh_client(server=server, password = password)
    
    print "start socket5 forward at localhost prot %s" % local_port
    
    class subhandler(Handler):
        ssh_transport = client.get_transport()
        
    try:
        server = SocketServer.ThreadingTCPServer(('', local_port), subhandler)
        server.daemon_threads = True
        server.allow_reuse_address = True
        print server.allow_reuse_address
        #server.timeout = 10
        #server.request_queue_size = 10
        server.serve_forever()
    except KeyboardInterrupt:
        print 'C-c: Port forwarding stopped.'
        sys.exit(0)

if __name__ == '__main__':
    main()