#!/bin/bash

for entry in "$1"*
do
        if [[ $entry == *".jpg" || $entry == *".png" ]] # only accept jpg or png files
        then
                if [[ $(stat -c%s "$entry") -lt 100 ]]
		then
			echo "less!"
	        	echo "$entry" >> empty_list.txt # write image paths into a temp file
		fi
        fi
done
