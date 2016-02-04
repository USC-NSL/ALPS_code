import urllib2

query_fov = "60"
query_key_google = "AIzaSyAdtMHxfsESr0OuVdGuseM_VW_uiDtahJY"
photo_dir = "./data/image_without_zoom/"

f_input = open("./data/generate_standing_point_output.txt", "r")
f_output = open("./data/download_photo_without_zoom_output.txt", "w")

class node():
	def __init__(self, id, lat, lng):
		self.id = str(id)
		self.lat = float(lat)
		self.lng = float(lng)

def save_photo(photo_url, photo_dir, photo_name):
	fjpg = open(photo_dir + photo_name, "wb")
	fjpg.write(urllib2.urlopen(photo_url).read())
	fjpg.close()

	f_output.write("%s\n" % photo_name)
	f_output.write("%s\n" % photo_url)

def calibrate_bearing(bearing):
	return (float(90) - float(bearing))

def download_zoom_photo(node3, bearing0, way_index, node_index):
	bearing0 = calibrate_bearing(bearing0)
	for k in range(6):
		bearing = bearing0 + k * 60

		query_lat = str(node3.lat)
		query_lng = str(node3.lng)
		query_heading = str(bearing)

		photo_url = "https://maps.googleapis.com/maps/api/streetview?size=900x900&location=%s,%s&fov=%s&heading=%s&pitch=0&key=%s" % (query_lat, query_lng, query_fov, query_heading, query_key_google)
		photo_name = "%s_%s_%s_%s_%s_%s.jpg" % (node3.id.zfill(12), str(way_index).zfill(2), str(node_index).zfill(2), query_lat, query_lng, query_heading)

		save_photo(photo_url, photo_dir, photo_name)

# ====== main =====
if __name__ == '__main__':

	while (f_input.readline()):
		intersection_id = f_input.readline().rstrip()
		tmp = f_input.readline().rstrip().split(',')
		node0 = node(intersection_id, tmp[0], tmp[1])
		download_zoom_photo(node0, float(0), 0, 0)

		node_on_ways = (int)(f_input.readline().rstrip())
		for way_index in range(1, (node_on_ways + 1), 1):
			bearing = float(f_input.readline().rstrip())
			for node_index in range(1, 8, 1):
				tmp = f_input.readline().rstrip().split(',')
				node3 = node(intersection_id, tmp[0], tmp[1])
				download_zoom_photo(node3, bearing, way_index, node_index)

	







