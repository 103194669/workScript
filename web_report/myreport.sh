#!/bin/bash
vmstat 1 2|awk '{cpuidel=$(NF-2);iowait=$(NF-1)}END{printf("cpuidel=%s iowait=%s",cpuidel,iowait)}'
awk '{printf " loadavg="$1}' /proc/loadavg 
awk -F"[ :]+" 'NR==5{printf " swap="$2/1024}' /proc/meminfo
netstat -an|awk '/^tcp/{a[$6]++}END{printf " max_conn="a["ESTABLISHED"]}'
printf "\n"
