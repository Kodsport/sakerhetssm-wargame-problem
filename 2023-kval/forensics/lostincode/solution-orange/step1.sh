#!/bin/bash

filename=flag

rm -r tmp
mkdir tmp
cp $filename tmp
cd tmp

while [ 1 ]
do
        file $filename
        file $filename | grep "bzip2"
        if [ "$?" -eq "0" ]
        then
                echo "This is Bzip!"
                mv $filename $filename.bz2
                bunzip2 -qq $filename.bz2
                filename=$(ls *)
        fi
        file $filename | grep "Zip"
        if [ "$?" -eq "0" ]
        then
                echo "This is Zip!"
                mv $filename $filename.zip
                unzip -qq $filename.zip
                rm $filename.zip
                filename=$(ls *)
        fi
        file $filename | grep "ASCII"
        if [ "$?" -eq "0" ]
        then
                echo "This is ASCII!"
                tail -c 100 $filename
                tail -c 100 $filename | grep " "
                if [ "$?" -eq "0" ]
                then
                        cat $filename
                        break
                fi
                openssl base64 -d -in $filename -out $filename.new
                rm $filename
                filename=$(ls *)
        fi
        file $filename | grep "gzip"
        if [ "$?" -eq "0" ]
        then
                echo "This is gzip!"
                mv $filename $filename.gz
                gunzip -qq $filename.gz
                filename=$(ls *)
        fi
done

