import math
import utm
import numpy as np

def calibrate_heading(heading):
	if heading < 270:
		bearing = 90 - heading
	else:
		bearing = 450 - heading

	return bearing


# ====== main =====
if __name__ == '__main__':

	query_fov = float(60.0)
	photo_pixel = float(640.0)

	f_input = open("./log.txt", "r")
	f_output = open("./triangulation_output.txt", "w")

	landmark_num = 123

	for i in range(landmark_num):
		f_output.write("=== play with the %dth intersection ===\n" % i)

		mysin = []
		mycos = []
		x = []
		y = []

		detected_image_num = 0

		for image_index in range(20):
			photo_path = f_input.readline().rstrip()
			logo_detection_result = f_input.readline().rstrip()

			if (logo_detection_result != "NULL"):
				detected_image_num += 1

				tmp = photo_path.split('_')
				view_lat = float(tmp[2])
				view_lng = float(tmp[3])
				view_heading = float(tmp[4][:-4])

				# print "(%s, %s, %s)" % (view_lat, view_lng, view_heading)

				logo_pixel = float(logo_detection_result)

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

		f_output.write("get %d detected photo\n" % detected_image_num)
		if (detected_image_num < 4):
			f_output.write("Haven't enough images...\n")
		else:
			G = []

			for i in range(detected_image_num):
				G.append(mysin[i])
				G.append(-mycos[i])

			G = np.reshape(G, (detected_image_num, 2))

			h = []

			for i in range(detected_image_num):
				h.append(x[i] * mysin[i] - y[i] * mycos[i])

			h = np.reshape(h, (detected_image_num, 1))

			tmp1 = G.transpose()
			tmp2 = np.dot(tmp1, G)
			tmp3 = np.linalg.inv(tmp2)
			tmp4 = np.dot(tmp3, tmp1)
			theta = np.dot(tmp4, h)

			# tmp = utm.from_latlon(34.023061, -118.279284)
			tmp = utm.from_latlon(view_lat, view_lng)
				
			tmp2 = utm.to_latlon(theta[0][0], theta[1][0], tmp[2], tmp[3])
			f_output.write('%s,%s\n' % (str(tmp2[0]), str(tmp2[1])))		
