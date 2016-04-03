import math
import utm
import numpy as np

def heading_to_theta(heading):
	theta = 90 - heading
	return theta

# ====== main =====
if __name__ == '__main__':

	f_input = open("detection_result_119.txt", "r")
	f_output = open("triangulation_output_119.txt", "w")

	image_num = 7

	for i in range(1):

		mysin = []
		mycos = []
		x = []
		y = []
		
		for j in range(image_num):
			image_path = f_input.readline().rstrip()[:-4]
			logo_detection_result = f_input.readline().rstrip()

			if (logo_detection_result[0] == "n"):
				for k in range(3):
					f_input.readline()
					f_input.readline()
				break

			tmp = image_path.split("_")
			view_lat = float(tmp[2])
			view_lng = float(tmp[3])
			# query_fov = float(tmp[4])
			query_fov = 60.0
			view_heading = float(tmp[4])
			# view_pitch = float(tmp[6])

			tmp = logo_detection_result.split('/')
			photo_pixel_width = float(tmp[0])
			photo_pixel_height = float(tmp[1])
			logo_pixel_left = float(tmp[2])
			logo_pixel_right = float(tmp[3])
			logo_pixel_top = float(tmp[4])
			logo_pixel_down = float(tmp[5])

			logo_pixel_horizontal = (logo_pixel_left + logo_pixel_right) / 2

			distance_pixel = photo_pixel_width / (2 * math.tan(0.5 * query_fov * math.pi / 180))

			relative_heading = math.atan2(logo_pixel_horizontal - photo_pixel_width / 2, distance_pixel) * 180 / math.pi
			view_heading_new = view_heading + relative_heading

			theta = heading_to_theta(view_heading_new) * math.pi / 180

			mysin.append(math.sin(theta))
			mycos.append(math.cos(theta))

			xy = utm.from_latlon(view_lat, view_lng)

			x.append(xy[0])
			y.append(xy[1])

		if (len(x) == image_num):
			G = []

			for i in range(image_num):
				G.append(mysin[i])
				G.append(-mycos[i])

			G = np.reshape(G, (image_num, 2))

			h = []

			for i in range(image_num):
				h.append(x[i] * mysin[i] - y[i] * mycos[i])

			h = np.reshape(h, (image_num, 1))

			tmp1 = G.transpose()
			tmp2 = np.dot(tmp1, G)
			tmp3 = np.linalg.inv(tmp2)
			tmp4 = np.dot(tmp3, tmp1)
			theta = np.dot(tmp4, h)

			tmp = utm.from_latlon(view_lat, view_lng)
					
			tmp2 = utm.to_latlon(theta[0][0], theta[1][0], tmp[2], tmp[3])

			f_output.write("%s,%s\n" % (str(tmp2[0]), str(tmp2[1])))
		else:
			f_output.write("can't localize...\n")