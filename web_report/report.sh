#!/bin/bash

export PATH=/usr/kerberos/sbin:/usr/kerberos/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/X11R6/bin:/usr/local/php/bin:/root/bin:/home/tangweizhong/shell/bin
DATE=`date +%F`
MONTH=`date +%m`
YEAR=`date +%Y`
rm -f system-report-$DATE.html
for ip in `awk 'BEGIN{RS="#";FS="\n"}NR>1{i=1;while(++i<NF)print $1"="$i}' iplist`
do
    printf "%s " ${ip%=*}
    printf "%s " ${ip#*=}
#sh myreport.sh
awk '/CPU.*idle/{
    while(1){
        getline;
        if($NF){
            idle=$6>idle?$NF:idle;
            iowait=$5>iowait?$5:iowait
        }else 
            break
        }
    }/run/{
    while(1){
        getline;
        if($0!=""&&NR!=a){
            loadavg=$NF>loadavg?$NF:loadavg
        }else{
            break
            }
        ;a=NR
        }
    }/IFACE.*rxmcst/{
    while(1){
        getline;
        if($0!=""){
            rxbyt=$5>rxbyt?$5:rxbyt;
            txbyt=$6>txbyt?$6:txbyt}else break
        }
    }/kbmemfree/{
    while(1){
        getline;if($0!=""){
        swap=$9>swap?$9:swap
    }else 
        break
    }
}END{
printf("idle=%s iowait=%s loadavg=%s rxbyt=%s txbyt=%s swap=%s\n",idle,iowait,loadavg,rxbyt,txbyt,swap)
}' sar02 
done |awk '
BEGIN{
    warn["max_conn"]=2
    warn["swap"]=5
    FS="[ =]"
}
{
a[$1,NR,"ip"]=$2
b[$1,"1"]="ip"
c[$1]
for(i=3;i<NF;i++){
    j=i
    b[$1,i]=$i
    a[$1,NR,$j]=$(++i)
    }
}
END{
    step=1
    print "<html>"
	print "<body>"
    for(group in c){
	    print "<h1>"group" SYSTEM REPORT</h1>"
        step+=(NR/length(c))
        print "<table>"
        for(i=1;i<NF;i=i+2){
            print "<tr>"
            print "<td Bgcolor=#FFCC33 align=right >"b[group,i]"</td>"
            for(j=step-NR/length(c);j<step;j++){
                if(warn[b[group,i]]>0&&a[group,j,b[group,i]]>warn[b[group,i]]){
                    print "<td Bgcolor=red align=right>"a[group,j,b[group,i]]"</td>"
                }else{
                    print "<td Bgcolor=#CCFFFF align=right>"a[group,j,b[group,i]]"</td>"
                }
            }
            print "</tr>"
        }
        print "</table>"
    }   
    print "</body>"
    print "</html>"
}' >> system-report-$DATE.html
