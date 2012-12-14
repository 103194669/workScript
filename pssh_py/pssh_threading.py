import paramiko, socket, threading
from config import config
nconnect = []

def ssh_client(info):
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        s.connect(info[0], 22, 'root', info[1])           
    except paramiko.AuthenticationException:
        nconnect.append("connect to address %s password Error!" % info[0])
        s = None
    return s

def report():
    if nconnect:
        for i in nconnect:
            print i
    else:
        print "all is ok!"

def main():
    thread_pool = []
    cmd = ''' netstat -ntlp|grep 6379 '''
    for info in config:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(100)
        try:
            sk.connect((info[0], 22))
        except :
            nconnect.append("connect to address %s on Port 22!" % info[0])
            sk.close()
        else:
            thread_pool.append(commandThread(info, cmd))      
    for work in thread_pool:
        work.start()
    for work in thread_pool:
        work.join()                       
    
class commandThread(threading.Thread):
    def __init__(self, info, cmd):
        threading.Thread.__init__(self)
        self.info = info
        self.cmd = cmd
        
    def run(self):
        client = ssh_client(self.info)
        if client:
            stdin, stdout, stderr = client.exec_command(self.cmd)
            error = stderr.read()
            if error:
                print '''==============%s============================
%s is false
%s
==============END============================
''' % (self.info[2], self.info[0], error)
                nconnect.append('''%s command "%s" Error!''' % (self.info[0], self.cmd))
            else:
                print '''==============%s==================================
%s is ok
%s
==============END============================                
''' % (self.info[2], self.info[0], stdout.read())
            client.close()
        client.close()        
 
if __name__ == "__main__":
    main()
    report()
