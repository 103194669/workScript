#!/usr/bin/env python
import urllib2
import hashlib
import time
import sys

def md5(data):
    d = hashlib.md5()
    d.update(data)
    return d.hexdigest()

def get_js(ip):
    request = urllib2.Request("http://%s/bitauto/Bitauto.Login.Version3.js?10"
            % ip, headers = {"Host":"js.inc.baa.bitautotech.com"})
    response = urllib2.urlopen(request)
    data = response.read()
    return md5(data)

def main():
    newmd5 = {}
    md5key = {}
    oldmd5 = 0

    try:    
        f = open("md5sum")
        oldmd5 = f.read()
    except IOError:
        pass

    for ip in ["59.151.127.40", "59.151.127.45", "js.inc.baa.bitautotech.com"]:
        md5 = get_js(ip)
        md5key[md5] = ip
        newmd5[ip] = md5
    
    if len(md5key) == 1 and md5 == oldmd5:
        print "ok"
        sys.exit(0)
    elif len(md5key) == 1 and md5 != oldmd5:
        f = open("md5sum", "w")
        f.write(md5)
        f.close()
        f = open("oldmd5", "a")
        f.write("%s %s\n" % (time.time(), oldmd5))
        f.close()
        print "not oldmd5"
        sys.exit(1)
    elif len(md5key) != 1:
        f = open("difmd5", "w")
        for key, m in newmd5.items():
            f.write("%s %s %s\n" % (time.time(), key, m))
        f.close()
        print "diffents"
        sys.exit(1)
    else:
        f = open("md5sum", "w")
        f.write(md5)
        f.close()
        print "oldmd5 is none"
        sys.exit(0)
    
if __name__ == "__main__":
    main()
