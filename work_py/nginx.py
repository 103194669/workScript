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
                get_line(f) 

def add_key(num, block):
    global key
    global block_num
    global block_list
    b_s = block.split("}")
        
    for i in xrange(len(b_s)):
        if b_s[i]:
            key = key + 10**(18-(block_num*3))
            b = re.split(r"[\t ]+", b_s[i].strip())
            if b[0] == "include":
                include(b[1])
            else:
                b_t = ""
                b_start = ""
                b_b = []
                for j in xrange(len(b)):
                    print j
                    if b[j].startswith("'") and (b[j].count("'") - b[j].count(r"\'"))%2:
                        b_start = "'"
                        b_t = b[j]
                    elif b[j].startswith('"') and (b[j].count('""') - b[j].count(r'\"'))%2:
                        b_start = '"'
                        b_t = b[j]
                    elif b_start:
                        b_t += b[j]
                        if b[j].endswith(b_start):
                            b_b.append(b_t)
                            b_start = ""
                    else:
                        b_b.append(b[j])
                block_list[key] = b
        if i:
            block_num -= 1
            key = key / (10**(18-((block_num)*3))) * (10**(18-((block_num)*3)))

def split_line(line):
    l = line.strip(" ;")
    if l:
        l = l.split(";")
        l_l = ""
        for i in xrange(len(l)):
            if l[i].endswith("\\"):
                l_l += l[i]
            elif l_l:
                add_key(i, l_l)
            else:
                add_key(i, l[i])

def get_line(f):
    global key
    global block_num
    global block_list
    
    try:
        f = open(f)
    except Exception, e:
        print e

    tmp_line = ""
    for line in f:
        line = line.strip()
        line = line.split("#")[0].strip()
        if line.endswith(";") or line.endswith("}"):
            tmp_line += line
            l = tmp_line.split("{")
            for i in xrange(len(l)):
                if i:
                    block_num += 1
                split_line(l[i])
            tmp_line = ""
        else:
            tmp_line += line

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
    get_line(CONF)
    list = sorted(block_list.items(), key=lambda d: d[0])
    for i in list:
        print i

if __name__ == "__main__":
    main()
