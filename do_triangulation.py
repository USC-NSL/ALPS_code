import math
import utm
import numpy as np

from datetime import datetime

def calibrate_heading(heading):
	if heading < 270:
		bearing = 90 - heading
	else:
		bearing = 450 - heading

	return bearing




# ====== main =====
if __name__ == '__main__':

	query_name = open('./config/query_name.info').readline().rstrip()	# ex. subway
	query_zip = open('./config/query_zip.info').readline().rstrip()			# ex. CA 90007
	# query_zip = 'NY10001'
	query_fov = open('./config/query_fov.info').readline().rstrip()		# ex. 60
	query_fov = float(query_fov)

	# zoom_flag = True
	# if (not zoom_flag):
	# 	query_name_dir = query_name
	# else:
	# 	query_name_dir = '%s_with_merge' % query_name

	# work_dir = './data/%s/' % query_name_dir
	work_dir = './data/%s/%s/' % (query_name, query_zip)

	f_input = open(work_dir + 'do_logo_detection_meta.txt', 'r')
	f_meta = open(work_dir + 'do_triangulation_meta.txt', 'w')

	# print work_dir

	landmark_index = 0

	while (f_input.readline()):

		if (landmark_index > 1000):
			break

		f_meta.write('=== play with the %dth landmark ===\n' % landmark_index)
		print '=== play with the %dth landmark ===' % landmark_index

		f_input.readline()

		mysin = []
		mycos = []
		x = []
		y = []

		detected_photo_num = 0

		for i in range(20):
			photo_path = f_input.readline().rstrip()
			logo_detection_result = f_input.readline().rstrip()

			if (len(logo_detection_result.split('/')) == 4):

				detected_photo_num += 1

				tmp = photo_path.split('/')[-1].split('_')
				view_lat = float(tmp[2])
				view_lng = float(tmp[3])
				view_heading = float(tmp[4][:-4])

				# print '%s,%s' % (view_lat, view_lng)
				# print view_heading

				tmp = logo_detection_result.split('/')
				photo_pixel = float(tmp[2])
				logo_pixel = 0.5 * (float(tmp[0]) + float(tmp[1]))

				distance = photo_pixel / (2 * math.tan(0.5 * query_fov * math.pi / 180))
				relative_bearing = math.atan2(logo_pixel - photo_pixel / 2, distance) * 180 / math.pi

				bearing = calibrate_heading(view_heading)
				alpha = bearing - relative_bearing

				alpha = alpha * math.pi / 180

				mysin.append(math.sin(alpha))
				mycos.append(math.cos(alpha))

				xy = utm.from_latlon(view_lat, view_lng)

				x.append(xy[0])
				y.append(xy[1])

		f_meta.write('get %d detected photo\n' % detected_photo_num)
		if (detected_photo_num < 4):
			f_meta.write('Haven\' enough photo...\n')
			print 'Haven\' enough photo...'
		else:
			G = []

			for i in range(detected_photo_num):
				G.append(mysin[i])
				G.append(-mycos[i])

			G = np.reshape(G, (detected_photo_num, 2))

			h = []

			for i in range(detected_photo_num):
				h.append(x[i] * mysin[i] - y[i] * mycos[i])

			h = np.reshape(h, (detected_photo_num, 1))

			tmp1 = G.transpose()
			tmp2 = np.dot(tmp1, G)
			tmp3 = np.linalg.inv(tmp2)
			tmp4 = np.dot(tmp3, tmp1)
			theta = np.dot(tmp4, h)

			# tmp = utm.from_latlon(34.023061, -118.279284)
			tmp = utm.from_latlon(view_lat, view_lng)
				
			tmp2 = utm.to_latlon(theta[0][0], theta[1][0], tmp[2], tmp[3])
			f_meta.write('%s,%s\n' % (str(tmp2[0]), str(tmp2[1])))
			print '%s,%s' % (str(tmp2[0]), str(tmp2[1]))

		landmark_index += 1

	# tend = datetime.now()
	# print tend
	# f_meta.write('%s\n' % str(tend))