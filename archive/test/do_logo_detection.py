import glob
import math
import utm
import numpy as np

import time, os, copy, sys, random, threading
from datetime import datetime

RESULT_HEADER = "RESULT: "
ERROR_MSG = "ERROR"

WSIZE_WIDTH = 120 # window size
WSIZE_HEIGHT = 36

BSIZE_WIDTH = 12
BSIZE_HEIGHT = 12

BSTRIDE_WIDTH = 6
BSTRIDE_HEIGHT = 6

CSIZE_WIDTH = 6
CSIZE_HEIGHT = 6

CODE_DIR = 'code_with_zoom'
RES_DIR = './data/detected_photo/'
THRESHOLD = 1.20

if not os.path.exists(RES_DIR):
	os.makedirs(RES_DIR)

def get_result(image_path, logo_name, store_img = 1, res_dir_path= RES_DIR):
	cmd = './%s/detect/detect ' % CODE_DIR + `THRESHOLD` + ' ' + image_path + ' %s/descriptors/' % CODE_DIR + logo_name + '.dat ' + `store_img` + ' ' + res_dir_path + \
	' ' + `WSIZE_WIDTH` + ' ' + `WSIZE_HEIGHT` + ' ' + `BSIZE_WIDTH` + ' ' + `BSIZE_HEIGHT` + \
	' ' + `BSTRIDE_WIDTH` + ' ' + `BSTRIDE_WIDTH` + ' ' + `CSIZE_WIDTH` + ' ' + `CSIZE_HEIGHT`

	ret_val = os.popen(cmd).read().split('\n') # system call
	found = False
	for i in range(len(ret_val)):
		# print ret_val[i]
		if ret_val[i].startswith(RESULT_HEADER): # if result starts with RESULT means success
			found = True
			return ret_val[i].split(RESULT_HEADER)[-1] # return result
			break
	if found == False:
		# print 'error!'
		return ERROR_MSG # not found, return ERROR

def calibrate_heading(heading):
	if heading < 270:
		bearing = 90 - heading
	else:
		bearing = 450 - heading

	return bearing

# ====== main =====
if __name__ == '__main__':

	query_name = "subway"

	photo_dir = "./data/image_merged/"

	f_output = open("./data/do_logo_detection_output.txt", "w")

	# get landmark_num in total
	tmp_format = photo_dir + '*.jpg'
	intersection_id_array = []
	intersection_num = 0
	previous_file_num = -1
	for file_name in sorted(glob.glob(tmp_format)):
		file_tmp = file_name.split('/')[-1][0:12]
		file_num = int(file_tmp)
		if (file_num != previous_file_num):
			intersection_num += 1
			previous_file_num = file_num
			intersection_id_array.append(str(file_num).zfill(12))

	# print intersection_num
	for intersection_index in range(intersection_num):
		# print "\t%s" % intersection_id_array[i]
		tmp_format = photo_dir + "%s_*.jpg" % intersection_id_array[intersection_index]
		f_output.write("=== play with the %dth intersection ===\n" % intersection_index)
		print "=== play with the %dth intersection ===" % intersection_index
		f_output.write("this intersection's id is %s\n" % intersection_id_array[intersection_index])
		print "this intersection's id is %s" % intersection_id_array[intersection_index]
		image_num = len(glob.glob(tmp_format))
		f_output.write("there are %d images for this intersection in total\n" % image_num)
		print "there are %d images for this intersection in total" % image_num

		# for file_name in sorted(glob.glob(tmp_format)):
		# 	file_tmp = file_name.split('/')[-1][:-4]#.split('_')
		# 	# print file_tmp

		detected_image_num = 0
		photo_path_array = []
		logo_detection_result_array = []
		for photo_path in sorted(glob.glob(tmp_format)):
			logo_detection_result = get_result(photo_path, query_name, 1)

			if (len(logo_detection_result.split('/')) == 4):
				detected_image_num += 1

			photo_path_array.append(photo_path)
			print photo_path
			logo_detection_result_array.append(logo_detection_result)
			print logo_detection_result

		f_output.write("there are %d images detected for this intersection\n" % detected_image_num)
		print "there are %d images detected for this intersection" % detected_image_num
		for photo_index in range(len(photo_path_array)):
			f_output.write("%s\n" % photo_path_array[photo_index])
			f_output.write("%s\n" % logo_detection_result_array[photo_index])





















