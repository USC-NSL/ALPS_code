for entry in "$1"*
do
	if [[ $entry == *".jpg" || $entry == *".png" ]] # only accept jpg or png files
	then
		echo "$entry" >> train.txt # write image paths into a temp file
	fi
done
