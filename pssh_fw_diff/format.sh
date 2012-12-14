#!/bin/bash
OUT_DIR=./fw
IN_DIR=./report
mkdir -p $OUT_DIR
for i in `ls $IN_DIR`;do
#    awk '/fw.sh/{
#while(1){
#    getline;if($0~"exit"){exit}else{print $0}
#    }
#}' 
grep "/sbin/iptables" $IN_DIR/$i >$OUT_DIR/${i%_*}
done
