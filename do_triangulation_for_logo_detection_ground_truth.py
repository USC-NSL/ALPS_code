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

	query_fov = open('./config/query_fov.info').readline().rstrip()		# ex. 60
	query_fov = float(query_fov)

	work_dir = './data/%s/%s/' % (query_name, query_zip)

	f_meta = open(work_dir + 'do_triangulation_for_logo_detection_ground_truth_meta.txt', 'w')

	with open(work_dir + 'logo_detection_ground_truth.txt', 'r') as f_input:
		
		current_landmark_index = 0
		
		mysin = []
		mycos = []
		x = []
		y = []

		detected_photo_num = 0

		for line in f_input:
			line_tmp = line.rstrip()
			# print line_tmp

			landmark_index = int(line_tmp[0:3])
			if (landmark_index != current_landmark_index):

				print "=== play with the %dth landmark ===" % current_landmark_index
				print "get %d detected photo" % detected_photo_num
				f_meta.write("=== play with the %dth landmark ===\n" % current_landmark_index)
				f_meta.write("get %d detected photo\n" % detected_photo_num)

				if (detected_photo_num >= 4):
					# do triangulation
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
				else:
					# not enough photo
					f_meta.write('Haven\' enough photo...\n')
					print 'Haven\' enough photo...'

				for i in range(landmark_index - current_landmark_index - 1):
					print "=== play with the %dth landmark ===" % (current_landmark_index + i + 1)
					print "get %d detected photo" % 0
					print 'Haven\' enough photo...'
					f_meta.write("=== play with the %dth landmark ===\n" % (current_landmark_index + i + 1))
					f_meta.write("get %d detected photo\n" % 0)
					f_meta.write('Haven\' enough photo...\n')

				# initialize again...
				current_landmark_index = landmark_index

				mysin = []
				mycos = []
				x = []
				y = []

				detected_photo_num = 0

			detected_photo_num += 1
			tmptmp = line_tmp.split(' ')
			tmptmp1 = tmptmp[0].split('_')
			view_lat = float(tmptmp1[2])
			view_lng = float(tmptmp1[3])
			view_heading = float(tmptmp1[4][:-4])

			tmptmp2 = tmptmp[1].split(',')
			photo_pixel = float(tmptmp2[0])
			logo_pixel = 0.5 * (float(tmptmp2[1]) + float(tmptmp2[2]))

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






