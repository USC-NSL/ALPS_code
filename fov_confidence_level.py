import os
import math
import urllib2

query_key_google = open("./config/query_google_key.info", "r").readline().rstrip()
query_city = open("./config/query_city.info", "r").readline().rstrip()

work_dir = "./data/%s/" % query_city

image_dir = work_dir + "confidence_level_with_different_zoom/"
if not os.path.exists(image_dir):
	os.makedirs(image_dir)

f_input = open(work_dir + "mtv_v3_processed.txt", "r")
f_output = open(work_dir + "fov_confidence_level_output.txt", "w")

query_fov = float("20")

def save_photo(photo_url, photo_dir, photo_name):
	f_output.write("%s\n" % photo_name)
	print photo_name
	f_output.write("%s\n" % photo_url)

	fjpg = open(photo_dir + photo_name, "wb")
	fjpg.write(urllib2.urlopen(photo_url).read())
	fjpg.close()


# ====== main =====
if __name__ == '__main__':

	image_number = 85

	for image_index in range(image_number):
		image_path = f_input.readline().rstrip()
		logo_detection_result = f_input.readline().rstrip()

		# if (int(image_path[0:6]) < 975):
		# 	continue

		tmp = image_path[:-4].split('_')
		view_lat = float(tmp[4])
		view_lng = float(tmp[5])
		view_heading = float(tmp[6]) + float(tmp[7][1:])
		view_pitch = float(tmp[8][1:])

		tmp = logo_detection_result.split('/')
		photo_pixel_width = float(tmp[0])
		photo_pixel_height = float(tmp[1])
		logo_pixel_left = float(tmp[2])
		logo_pixel_right = float(tmp[3])
		logo_pixel_top = float(tmp[4])
		logo_pixel_down = float(tmp[5])

		logo_pixel_horizontal = (logo_pixel_left + logo_pixel_right) / 2
		logo_pixel_vertical = (logo_pixel_top + logo_pixel_down) / 2
		logo_pixel_vertical = photo_pixel_height - logo_pixel_vertical


		distance_pixel = photo_pixel_width / (2 * math.tan(0.5 * query_fov * math.pi / 180))

		relative_heading = math.atan2(logo_pixel_horizontal - photo_pixel_width / 2, distance_pixel) * 180 / math.pi
		relative_pitch = math.atan2(logo_pixel_vertical - photo_pixel_height / 2, distance_pixel) * 180 / math.pi

		view_heading_new = view_heading + relative_heading
		view_pitch_new = view_pitch + relative_pitch

		for query_fov_new in range(20, 8, -2):
			photo_url = "https://maps.googleapis.com/maps/api/streetview?size=900x900&location=%s,%s&fov=%s&heading=%s&pitch=%s&key=%s" % (view_lat, view_lng, query_fov_new, view_heading_new, view_pitch_new, query_key_google)
			save_photo(photo_url, image_dir, "%s_fov%d.jpg" % (image_path[:-4], query_fov_new))

