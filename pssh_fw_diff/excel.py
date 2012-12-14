#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import xlwt

def get_data():
    data = [] 
    for type in os.listdir('result'):
        print type
        if os.path.isdir(os.path.join("result", type)):
            d = []
            c = []
            d.append(type)
            for line in open(os.path.join("result", type, "server")):
                c.append(line)
            d.append(c)
            data.append(d)
        else:
            d = []
            c = []
            d.append(type)
            for line in open(os.path.join("result", type)):
                c.append(line)
            d.append(c)
            data.append(d)
    return data

def report():
    data = get_data()
    book = xlwt.Workbook()
    sheet = book.add_sheet("fw report")
    sheet.panes_frozen = True
    sheet.horz_split_pos = 1
    sheet.write(0,0,"type")
    sheet.write(0,1, "ip")
    i = 1
    for j in data:
        sheet.write(i,0,j[0])
        for k in j[1]:
            sheet.write(i, 1, k)
            i+=1
    book.save('report.xls')

if __name__ == "__main__":
    report()
