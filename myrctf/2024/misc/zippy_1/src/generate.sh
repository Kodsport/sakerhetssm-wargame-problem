#!/bin/bash

mkdir archive
yq '.flag' challenge.yaml > archive/flag.txt

depth=300

ln=archive

for i in $(seq 1 $depth)
do

	cn=$(openssl rand -hex 6)
	zip -r --password $cn $cn.zip $ln &>/dev/null
	# zip -r $cn.zip $ln &>/dev/null

	rm $ln &>/dev/null
	ln=$cn.zip
	echo -ne "\r(Zipped $i/$depth)"
done

rm -rf archive
