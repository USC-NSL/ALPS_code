#!/bin/bash
# this script is used for creating the list of files
# $1: file_list.txt
# $2: image dir
# $3: dst dir

while IFS='' read -r line || [[ -n "$line" ]]; do
   # echo "Text read from file: $line"
    if [[ $line == *".jpg" ]]
    then
    	mv $2${line:0:(-4)}.png $3${line:0:(-4)}.png
    	
    fi
done < "$1"

echo "end"

