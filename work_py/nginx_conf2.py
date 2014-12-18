import re
import os
import sys


class ConfParse(object):

    def __init__(self, f):
        self.f = f
        self.block_list = {}
        self.key = 0
        self.single_syntax = ["server_name", "proxy_read_timeout", "access_log"]
        self.abs_path = os.path.dirname(f)

    def include(self, r):
        r = r.replace("*", ".*")
        p = os.path.join(self.abs_path, os.path.dirname(r))
        r = re.compile(r"%s$" % r)
        for root, dirs, files in os.walk(p):
            for f in files:
                f = os.path.join(root, f)
                if r.search(f):
                    self.f = f
                    self.get_char()

    def get_char(self):
        f_size = os.path.getsize(self.f)
        try:
            f = open(self.f)
        except Exception, e:
            print e

        c = ""
        c_previous = ""
        c_one = 0
        c_tow = 0
        block = ""
        b_list = []
        flag = 0
        c_flag = 1
        n_flag = 0
        for i in xrange(f_size):
            c_previous = c
            c = f.read(1)
            if c == "\n":
                n_flag = 0
                continue
            if n_flag:
                continue
            if c_previous != "\\" and c_flag:
                if c == "#":
                    n_flag = 1
                    continue
                if c == "{":
                    if block:
                        b_list.append(block)
                    block = ""
                    flag = 0
                    self.key += 1
                    self.block_list[self.key] = b_list
                    self.key = self.key * 1000
                    b_list = []
                    continue
                if c == "}":
                    self.key = self.key / 1000 
                    continue
                if c == ";":
                    b_list.append(block)
                    block = ""
                    flag = 0
                    self.key = self.key + 1
                    
                    if b_list[0] in self.single_syntax:
                        self.block_list[str(self.key / 1000) + b_list[0]] = b_list
                    else:
                        self.block_list[self.key] = b_list
                    if b_list[0] == "include":
                        self.include(b_list[1])
                    b_list = []
                    continue
            if c_previous != "\\":
                if c == "'" and not c_tow:
                    c_one += 1
                    c_flag = 0
                    if c_one == 2:
                        c_one = 0
                        c_flag = 1
                    block += c
                    continue
                if c == '"' and not c_one:
                    c_tow += 1
                    c_flag = 0
                    if c_tow == 2:
                        c_tow = 0
                        c_flag = 1
                    block += c
                    continue
            if c in " \t":
                if block  and c_flag:
                    b_list.append(block)
                    block = ""
                    #flag = 0
                elif not c_flag:
                    block += c
                else:
                    continue
            else:
                block += c
                #flag = 1

    def run(self):
        self.get_char()
        return self.block_list
        #return self.l

def get_synatx(b_l, k, n):
    try:
        return b_l[str(k) + n]
    except KeyError:
        if k:
            result = get_synatx(b_l, k/1000, n)
        else:
            result = "have_no"
    return result

def main():
    try:
        CONF = sys.argv[1]
    except Exception, e:
        print e
        sys.exit(1)

    a = ConfParse(CONF)
    block_list = a.run()
    #list = sorted(block_list.items(), key=lambda d: d[0])
    for i,j in block_list.items():
        if j[0] == "location":
            server_name = get_synatx(block_list, i, 'server_name')
            proxy_read_timeout = get_synatx(block_list, i, 'proxy_read_timeout')
            for host in server_name[1:]:
                print host,j[-1],proxy_read_timeout[-1]

if __name__ == "__main__":
    main()
