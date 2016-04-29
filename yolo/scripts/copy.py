import sys, os

# input: [log_txt] [img_dir] [dest_txt] - img_dir must has '/' at end!
# note: the img_dir contains images in '.png' format, but 'log.txt' has only jpg format
# 		so we need a convertion

SUFFIX = '.png'

if __name__ == '__main__':
	if len(sys.argv) != 4:
		sys.exit('ERROR: wrong argc! Should be [src_log] [src_dir] [dst_log]')
	if not os.path.exists(sys.argv[1]):
		sys.exit('ERROR: ' + sys.argv[1] + ' was not found!')
	if not os.path.exists(sys.argv[2]):
		sys.exit('ERROR: ' + sys.argv[2] + ' was not found!')
	print 'your input is: ' + sys.argv[1] + ' ' + sys.argv[2]
	# read the log_txt
	fin = open(sys.argv[1], 'r')
	line = fin.readline()
	fout = open(sys.argv[3], 'w')
	counter_pos = 0
	counter_neg = 0
	while line != '':
		if os.path.isfile(sys.argv[2] + line.split('\n')[0].split('.jpg')[0] + SUFFIX): # if the image exists
			counter_pos += 1
			fout.write(line) # write the file name line
			line = fin.readline()
			fout.write(line) # write the position line
		else:
			counter_neg += 1
			# print sys.argv[2] + line.split('\n')[0] + ' does not exist..'
			line = fin.readline() # skip the position line
		line = fin.readline() # go to the next file name
	print `counter_pos` + ' images written..'
	print `counter_neg` + ' images not written..'
	fin.close()
	fout.close()
	print 'done'
