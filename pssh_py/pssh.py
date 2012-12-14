import paramiko, socket
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
    cmd = ''' grep "id:3:initdefault:" /etc/inittab '''
    for info in config:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(100)
        try:
            sk.connect((info[0], 22))
        except :
            nconnect.append("connect to address %s on Port 22!" % info[0])
            sk.close()
        else:
            client = ssh_client(info)
            if client:
                stdin, stdout, stderr = client.exec_command(cmd)
                error = stderr.read()
                if error:
                    print '''==============%s============================
%s is false
%s
==============END============================
''' % (info[2], info[0], error)
                    nconnect.append('''%s command "%s" Error!''' % (info[0], cmd))
                else:
                    print '''==============%s==================================
%s is ok
%s
==============END============================                
''' % (info[2], info[0], stdout.read())

if __name__ == "__main__":
    main()
    report()
