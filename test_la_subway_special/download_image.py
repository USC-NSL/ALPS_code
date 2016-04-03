import urllib2
import os


photo_dir = "subway_special2/"
if not os.path.exists(photo_dir):
	os.makedirs(photo_dir)

def save_photo(photo_url, photo_dir, photo_name):
	print photo_name
	print photo_url
	# f_output.write("%s\n" % photo_name)
	# f_output.write("%s\n" % photo_url)

	fjpg = open(photo_dir + photo_name, "wb")
	fjpg.write(urllib2.urlopen(photo_url).read())
	fjpg.close()


# ====== main =====
if __name__ == '__main__':

	# query_fov = "60"
	query_google_key = "AIzaSyBranwjpavQoj2xAtn6qeRARxURQeTD13M"

	f_input = open("input2.txt", "r")

	for i in range(22):
		for j in range(4):

			# streetview_url = "https://www.google.com/maps/@34.0117531,-118.2827353,3a,75y,82.4h,92.42t/data=!3m6!1e1!3m4!1sl4ZdMdz4ZqcKfAc1hvs7fQ!2e0!7i13312!8i6656"
			streetview_url = f_input.readline().rstrip()

			tmp = streetview_url.split("@")[1].split("/")[0].split(',')

			query_lat = float(tmp[0])
			query_lng = float(tmp[1])
			query_fov = float(tmp[3][:-1])
			query_heading = float(tmp[4][:-1])
			query_pitch = float(tmp[5][:-1]) - 90

			# print query_lat
			# print query_lng
			# print view_fov
			# print query_heading
			# print query_pitch

			photo_url = "https://maps.googleapis.com/maps/api/streetview?size=900x900&location=%s,%s&fov=%s&heading=%s&pitch=%s&key=%s" % (query_lat, query_lng, query_fov, query_heading, query_pitch, query_google_key)
			# photo_name = "1.jpg"
			photo_name = "%s_%s_%s_%s_%s_%s_%s.jpg" % (str(i).zfill(3), str(j).zfill(3), query_lat, query_lng, query_fov, query_heading, query_pitch)

			save_photo(photo_url, photo_dir, photo_name)
