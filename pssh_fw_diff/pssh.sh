#!/bin/bash
function Separator(){
	case $1 in
	Blue)
		echo -e "\033[34m<============= $2 \
===============>\033[0m"
	;;
	Green)
		echo -e "\033[32m<============= $2 \
===============>\033[0m"
	;;
	Red)
		echo -e "\033[31m<============= $2 \
===============>\033[0m"
	;;
	esac
}
>result.out
while read line;do
	a=($line)
	Separator Red ${a[0]}
	./.RemoteLogin.exp ${a[0]} ${a[1]} ${a[2]} ${a[3]} ${a[4]} > report/$a"_fw"
    echo "${a[0]} $?">>result.out
done< ${1:-serverlist}
