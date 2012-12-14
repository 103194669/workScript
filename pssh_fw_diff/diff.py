#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
path = os.path.abspath(os.path.dirname(__file__))
result = os.path.join(path, "result")
fw = os.path.join(path, "fw")
templates = []

def finsh():
    '''
    all = []
    for i in templates:
        for j in i:
            flag = True
            if j not in all:
                for k in templates:
                    if j not in k:
                        flag = False
                if flag:
                    all.append(j)
    o = open(os.path.join(result, "all_fw.sh"), "a")
    print all
    for i in all:
        o.writelines(i)
    o.close()
 '''
    os.chdir(result)
    for dir in os.listdir(result):
        if os.path.isdir(dir):
            '''
            o = open(os.path.join(dir, "fw.sh"))
            data = o.readlines()
            for line in data:
                if line not in all:
                    oo = open(os.path.join(dir,"diffent"), "a")
                    oo.writelines(line)
                    oo.close
            o.close()
            '''
            count = len(open(os.path.join(dir, "server"), 'r').readlines())
            os.rename(dir, "%s_%s"% (dir, count))

def make_template(file, data):
    if len(data) > 1:
        template_dir = os.path.join(result, "fw_%s"% (len(templates)+1))
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)
        o = open(os.path.join(template_dir, "fw.sh"), "w")
        o.writelines(data)
        templates.append(data)
        o.close()
        o = open(os.path.join(template_dir, "server"), "w")
        o.writelines(file+"\n")
        o.close()
    else:
        o = open(os.path.join(result, "no_fw"), "a")
        o.writelines(file+"\n")
        o.close()
   
def diff(file, data):
    i = 0
    f = 0
    for tem in templates:
        i+=1
        if len(tem) == len(data):
            flag = True
            for line in data:
                if line not in tem:
                    flag = False
                    break
            for line in tem:
                if line not in data:
                    flag = False
                    break
            if flag:
                o = open(os.path.join(result, "fw_%s"% i, "server"), "a")
                o.writelines(file+"\n")
                o.close()
                break
            else:
                f+=1
        else:
            f+=1

    if f == len(templates):
        make_template(file, data)
     
def main():
    if not os.path.exists(result):
        os.makedirs(result)
    for file in os.listdir(fw):
        absfile = os.path.join(fw, file)    
        o = open(absfile)
        data = o.readlines()
        if templates and len(data) > 1:
            diff(file, data)
        else:
            make_template(file, data)
        o.close()
    
    finsh()
                
if __name__ == "__main__":
    main()
