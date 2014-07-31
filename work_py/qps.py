#!/usr/bin/env python

import time
import fileinput

last_sec = 0
count = 0
for line in fileinput.input():
    t = int(time.time())
    if last_sec != t:
        print 'QPS:', count
        last_sec = t
        count = 0
    else:
        count += 1
