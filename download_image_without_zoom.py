import urllib2
import os

query_city = open("./config/query_city.info", "r").readline().rstrip()

work_dir = "./data/%s/" % query_city

f_input = open(work_dir + "generate_standing_point_output.txt", "r")
f_output = open(work_dir + "download_image_without_zoom_output.txt", "w")

query_fov = "60"

query_key_google = open("./config/query_google_key.info", "r").readline().rstrip()

photo_dir = work_dir + "image_without_zoom/"
if  not os.path.exists(photo_dir):
	os.makedirs(photo_dir)


class node():
	def __init__(self, lat, lng, theta = 0):
		self.lat = float(lat)
		self.lng = float(lng)
		self.theta = float(theta)

def save_photo(photo_url, photo_dir, photo_name):
	f_output.write("%s\n" % photo_name)
	f_output.write("%s\n" % photo_url)

	fjpg = open(photo_dir + photo_name, "wb")
	fjpg.write(urllib2.urlopen(photo_url).read())
	fjpg.close()

def calibrate_bearing(bearing):
	return (float(90) - float(bearing))

def download_photo(tmp_node, way_index, way_id, node_index):
	query_lat = str(tmp_node.lat)
	query_lng = str(tmp_node.lng)

	bearing0 = calibrate_bearing(tmp_node.theta)

	for k in range(2):
		bearing = bearing0 + k * 180
		query_heading = str(bearing)

		photo_url = "https://maps.googleapis.com/maps/api/streetview?size=900x900&location=%s,%s&fov=%s&heading=%s&pitch=0&key=%s" % (query_lat, query_lng, query_fov, query_heading, query_key_google)
		photo_name = "%s_%s_%s_%s_%s_%s_%s.jpg" % (str(way_index).zfill(6), str(way_id).zfill(12), str(node_index).zfill(6), str(k).zfill(2), query_lat, query_lng, query_heading)

		save_photo(photo_url, photo_dir, photo_name)

# ====== main =====
if __name__ == '__main__':

	start_way_index = 0
	# end_way_index = 1000
	start_node_index = 0

	way_index = 0
	while (f_input.readline()):
		way_id = f_input.readline().rstrip()
		node_num = int(f_input.readline().rstrip())
		for i in range(node_num):
			tmp = f_input.readline().rstrip().split(",")
			tmp_lat = tmp[0]
			tmp_lng = tmp[1]
			tmp_theta = f_input.readline().rstrip()
			tmp_node = node(tmp_lat, tmp_lng, tmp_theta)

			if (way_index == start_way_index):
				if (i >= start_node_index):
					download_photo(tmp_node, way_index, way_id, i)
			if (way_index > start_way_index):
				download_photo(tmp_node, way_index, way_id, i)


		way_index += 1
