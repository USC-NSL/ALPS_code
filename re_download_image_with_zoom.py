import glob
import os
import urllib2


query_key_google = open("./config/query_google_key.info", "r").readline().rstrip()
query_city = open("./config/query_city.info", "r").readline().rstrip()
work_dir = "./data/%s/" % query_city
photo_dir_origin = work_dir + "mtv_no_seed_v2/"
photo_dir_new = work_dir + "mtv_no_seed_v3/"

if not os.path.exists(photo_dir_new):
	os.makedirs(photo_dir_new)


query_fov = float("20")



def save_photo(photo_url, photo_dir, photo_name):
	# f_output.write("%s\n" % photo_name)
	# print photo_name
	# f_output.write("%s\n" % photo_url)

	fjpg = open(photo_dir + photo_name, "wb")
	fjpg.write(urllib2.urlopen(photo_url).read())
	fjpg.close()


# ====== main =====
if __name__ == '__main__':

	format = photo_dir_origin + "*.png"

	for full_image_path in sorted(glob.glob(format)):

		tmp = full_image_path.split('/')[-1][:-4]
		image_name = tmp + ".jpg"
		print image_name
		tmp = tmp.split('_')

		view_lat = float(tmp[4])
		view_lng = float(tmp[5])
		view_heading = float(tmp[6]) + float(tmp[7][1:])
		view_pitch = float(tmp[8][1:])

		# print "%s,%s" % (view_lat, view_lng)
		# print view_heading
		# print view_pitch


		photo_url = "https://maps.googleapis.com/maps/api/streetview?size=900x900&location=%s,%s&fov=%s&heading=%s&pitch=%s&key=%s" % (view_lat, view_lng, query_fov, view_heading, view_pitch, query_key_google)
		save_photo(photo_url, photo_dir_new, image_name)