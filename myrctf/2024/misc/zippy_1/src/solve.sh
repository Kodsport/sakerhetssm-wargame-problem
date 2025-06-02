#!/bin/bash
#!CMD: ./solve.sh *.zip
[[ $1 == "" ]] && echo "Usage: $0 <archive.zip>" && exit 1

zip=$1
i=0

while true
do
	i=$(($i+1))

	[[ $zip == "" ]] && exit 0
	pass=$(echo $zip | sed 's/\.zip//')
	unzip -P $pass $zip &>/dev/null
	rm $zip
	zip=$(ls | grep *.zip | head -n 1)

	echo -ne "\r(Unzipped: $i)"
done
