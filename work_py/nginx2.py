import re
import os
import sys


def include(r):
    r = r.replace("*", ".*")
    p = os.path.join(abs_path, os.path.dirname(r))
    r = re.compile(r"%s$" % r)
    for root, dirs, files in os.walk(p):
        for f in files:
            f = os.path.join(root, f)
            if r.search(f):
                get_char(f)

def get_char(f):
    global key
    global block_num
    global block_list
    
    f_size = os.path.getsize(f)
    try:
        f = open(f)
    except Exception, e:
        print e
    
    c_p = ""
    c_one = 0
    c_tow = 0
    block = ""
    b_list = []
    flag = 0
    c_flag = 1
    n_flag = 0
    for i in xrange(f_size):
        c = f.read(1)
        if c == "\n":
            n_flag = 0
            continue
        #if c == "#" and c_flag:
        #    n_flag = 1
        #    continue
        if n_flag:
            continue
        if c_p != "\\" and c_flag:
            if c=="#":
                n_flag = 1
                continue
            if c=="{":
                block = ""
                flag = 0
                key = key + 10**(18-(block_num*3))
                block_list[key] = b_list
                b_list = []

                block_num += 1
                continue
            if c=="}":
                block_num -= 1
                key = key / (10**(18-((block_num)*3))) * (10**(18-((block_num)*3)))
                continue 
            if c==";":
                b_list.append(block)
                block = ""
                flag = 0
                key = key + 10**(18-(block_num*3))
                block_list[key] = b_list
                if b_list[0] == "include":
                    include(b_list[1])
                b_list = []
                continue
        if c_p != "\\":
            if c=="'":
                print c_tow
                c_one += 1
                c_flag = 0
                if c_one == 2:
                    c_one = 0
                    c_flag = 1
                block += c
                continue
            if c_tow=='"' and not c_one:
                c_tow += 1
                f_flag = 0
                if c_tow == 2:
                    c_tow = 0
                    c_flag = 1
                block += c
                continue
        if c in " \t":
            if flag and c_flag:
                b_list.append(block)
                block = ""
                flag = 0
            elif not c_flag:
                block += c
            else:
                continue
        else:
            block += c
            flag = 1

def main():
    global key
    global block_num
    global block_list
    global abs_path
    
    block_list = {}
    block_num = 0
    key = 10 ** 21
    try:
        CONF = sys.argv[1]
    except Exception,e:
        print e
        sys.exit(1)

    abs_path = os.path.dirname(CONF)
    get_char(CONF)
    list = sorted(block_list.items(), key=lambda d: d[0])
    for i in list:
        print i

if __name__ == "__main__":
    main()
