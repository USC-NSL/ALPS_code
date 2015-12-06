import glob
import math
import utm
import numpy as np

import time, os, copy, sys, random, threading
from datetime import datetime

CODE_DIR = 'code'

THRESHOLD = 1.15 # threshold for detection

RESULT_HEADER = "RESULT: "
ERROR_MSG = "ERROR"

RES_DIR = 'res/'

WSIZE_WIDTH = 120 # window size
WSIZE_HEIGHT = 36

BSIZE_WIDTH = 12
BSIZE_HEIGHT = 12

BSTRIDE_WIDTH = 6
BSTRIDE_HEIGHT = 6

CSIZE_WIDTH = 6
CSIZE_HEIGHT = 6

zoom_flag = False #*****************************************************************
if (not zoom_flag):
	CODE_DIR = 'code'
	RES_DIR = 'res/'
	THRESHOLD = 1.15
else:
	CODE_DIR = 'code_with_zoom'
	RES_DIR = 'res_with_zoom/'
	THRESHOLD = 1.20

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

	query_name = open('./config/query_name.info').readline().rstrip()	# ex. subway
	# query_fov = open('./config/query_fov.info').readline().rstrip()		# ex. 60
	# query_fov = float(query_fov)

	if (not zoom_flag):
		query_name_dir = query_name
	else:
		query_name_dir = '%s_with_merge' % query_name

	# print CODE_DIR
	# print RES_DIR

	# res = get_result('./data/subway_with_merge/photo/000_000_34.011796_-118.282736_89.453796.jpg', 'subway')
	# print res

	work_dir = './data/%s/' % query_name_dir
	# work_dir = './data/%s/' % 'subway_no_zoom'
	photo_dir = work_dir + 'photo/'

	f_meta = open(work_dir + 'do_logo_detection_meta.txt', 'w')

	tstart = datetime.now()
	print tstart
	f_meta.write('%s\n' % str(tstart))

	# get landmark_num in total
	tmp_format = photo_dir + '*.jpg'
	max_num = 0
	for file_name in sorted(glob.glob(tmp_format)):
		file_tmp = file_name.split('/')[-1][0:3]
		file_num = int(file_tmp)
		if file_num > max_num:
			max_num = file_num

	# print max_num

	for landmark_index in range(max_num + 1):

		if (landmark_index >= 1000):
			break

		f_meta.write('=== play with the %dth landmark ===\n' % landmark_index)
		print '=== play with the %dth landmark ===' % landmark_index

		view_array = []

		format = photo_dir + '%s_*.jpg' % str(landmark_index).zfill(3)

		if (len(glob.glob(format)) != 20):
			f_meta.write('Error...\n')
			print 'Error...'
		else:

			detected_photo_num = 0
			photo_path_array = []
			logo_detection_result_array = []

			for photo_path in sorted(glob.glob(format)):
				# print photo_path

				logo_detection_result = get_result(photo_path, query_name, 1)

				if (len(logo_detection_result.split('/')) == 4):
					detected_photo_num += 1

				photo_path_array.append(photo_path)
				logo_detection_result_array.append(logo_detection_result)

				# f_meta.write('%s\n' % str(photo_path))
				# print photo_path

				# f_meta.write('%s\n' % str(logo_detection_result))
				# print logo_detection_result

			f_meta.write('get %s detected photo\n' % str(detected_photo_num))
			print detected_photo_num

			for photo_index in range(len(photo_path_array)):
				f_meta.write('%s\n' % str(photo_path_array[photo_index]))
				print photo_path_array[photo_index]

				f_meta.write('%s\n' % str(logo_detection_result_array[photo_index]))
				print logo_detection_result_array[photo_index]






	tend = datetime.now()
	print tend
	f_meta.write('%s\n' % str(tend))

