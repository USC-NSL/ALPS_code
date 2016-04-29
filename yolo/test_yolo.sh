#!/bin/bash
# this script is used for creating the list of files
# $1: weights file's path
# $2: image dir

# check if log.txt exists
if [ -f log.txt ]; then
	echo "You have unprocessed log file! Do you want to proceed? [Y/n]"
	read input
	if [ "$input" == "Y" ]; then
		rm log.txt
		echo "Previous log.txt removed"
	else
		exit 1
	fi
fi

# check if img dest dir exists
if [ ! -d detect_res ]; then
	mkdir detect_res
else
	echo "You may have images in 'detect_res'! Do you want to remove them? [Y/n]"
	read input
	if [ "$input" == "Y" ]; then
		rm detect_res/*
		echo "all images removed"
	else
		exit 1
	fi
fi

for entry in "$2"*
do
	if [[ $entry == *".jpg" || $entry == *".png" ]] # only accept jpg or png files
	then
		echo "$entry" >> file_list.txt # write image paths into a temp file
	fi
done
echo "file_list.txt created"
./darknet yolo test cfg/yolo.cfg $1 < file_list.txt
rm file_list.txt
echo "end"
