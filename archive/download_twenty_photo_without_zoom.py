import os
import urllib2
import time

query_fov = "60"
query_key_google = "AIzaSyAdtMHxfsESr0OuVdGuseM_VW_uiDtahJY"
photo_dir = "./data/subway/CA94035/image_without_zoom/"

f = open("./data/subway/CA94035/generate_twenty_location_meta.txt", "r")
f_meta = open("./data/subway/CA94035/download_twenty_photo_without_zoom_output.txt", "w")

# def save_photo(photo_url, photo_path, photo_name, ftxt):
# 	fjpg = open(photo_path + photo_name, 'wb')
# 	fjpg.write(urllib2.urlopen(photo_url).read())
# 	fjpg.close()

# 	ftxt.write(photo_name + '\n')
# 	ftxt.write(photo_url + '\n')

def save_photo(photo_url, photo_dir, photo_name):
	fjpg = open(photo_dir + photo_name, "wb")
	fjpg.write(urllib2.urlopen(photo_url).read())
	fjpg.close()

	f_meta.write("%s\n" % photo_name)
	f_meta.write("%s\n" % photo_url)

def download_zoom_photo(addr, bearing, photo_index, landmark_index):
	# for i in range(-20, 40, 20):
	# 	for j in range(-5, 15, 10):
	# 		query_location = str(addr)
	# 		query_fov = str(query_fov)
	# 		query_heading = str(float(bearing) + i)
	# 		query_pitch = str(j)

	# 		query_heading_origin = str(bearing)
	# 		query_heading_index = str(i)
	# 		query_pitch_index = str(j)

	# 		photo_url =generate_url(query_location, query_fov, query_heading, query_pitch, query_key_google)
	# 		save_photo(photo_url, photo_dir, '%s_%s_%s_%s_h%s_p%s.jpg' % (str(landmark_index).zfill(3), str(photo_index).zfill(3), query_location.replace(',', '_'), query_heading_origin, query_heading_index, query_pitch_index), f_meta)

	query_heading = str(bearing)
	query_location = str(addr)

	photo_url = "https://maps.googleapis.com/maps/api/streetview?size=900x900&location=%s&fov=%s&heading=%s&pitch=0&key=%s" % (query_location, query_fov, query_heading, query_key_google)
	photo_name = "%s_%s_%s_%s.jpg" % (str(landmark_index).zfill(3), str(photo_index).zfill(3), query_location.replace(',', '_'), query_heading)
	save_photo(photo_url, photo_dir, photo_name)

# ====== main =====
if __name__ == '__main__':

	# sleep_time = 0.5

	# query_name = open('./config/query_name.info').readline().rstrip()	# ex. subway
	# query_zip = open('./config/query_zip.info').readline().rstrip()			# ex. CA 90007

	# query_fov = open('./config/query_fov.info').readline().rstrip()		# ex. 60
	# query_fov = '20'
	# query_key_google = open('./config/query_key_google.info').readline().rstrip()		# ex. AIzaSyAdtMHxfsESr0OuVdGuseM_VW_uiDtahJY

	# work_dir = './data/%s/%s/' % (query_name, query_zip)

	# photo_dir = work_dir + 'photo/'
	# if not os.path.exists(photo_dir):
	# 	os.makedirs(photo_dir)

	# f = open(work_dir + 'generate_twenty_location_meta.txt', 'r')
	# f_meta = open(work_dir + 'download_twenty_photo_with_zoom_meta.txt', 'w')

	landmark_index = 0

	fromNum = 0
	endNum = 1000

	while (f.readline()):

		# if landmark_index > 1:
		# 	break
		if (landmark_index < fromNum):
			for i in range(46):
				f.readline()
			landmark_index += 1
			continue

		if (landmark_index >= endNum):
			break


		photo_index = 0

		# ===== Begin of google =====
		# place_id
		place_id = f.readline().rstrip()
		# origin landmark lat-lng (no use for fetching photo ...)
		f.readline()
		# origin landmark paddr (no use for fetching photo ...)
		f.readline()

		# google caddr
		for i in range(5):
			caddr = f.readline().rstrip()
			caddr_bearing = f.readline().rstrip()
			# caddr_url = generate_url(caddr, query_fov, caddr_bearing, query_key_google)

			# # prevent sever error...
			# time.sleep(sleep_time)
			# # save_photo(caddr_url, photo_dir, '%s_%s_google_caddr_%s.jpg' % (str(landmark_index).zfill(3), place_id, str(i).zfill(3)), f_meta)
			# save_photo(caddr_url, photo_dir, '%s_%s_%s_%s.jpg' % (str(landmark_index).zfill(3), str(photo_index).zfill(3), caddr.replace(',', '_'), caddr_bearing), f_meta)
			
			download_zoom_photo(caddr, caddr_bearing, photo_index, landmark_index)
			photo_index += 1

		# google paddr
		for i in range(5):
			paddr = f.readline().rstrip()
			paddr_bearing = f.readline().rstrip()
			# paddr_url = generate_url(paddr, query_fov, paddr_bearing, query_key_google)

			# # prevent sever error...
			# time.sleep(sleep_time)
			# # save_photo(paddr_url, photo_dir, '%s_%s_google_paddr_%s.jpg' % (str(landmark_index).zfill(3), place_id, str(i).zfill(3)), f_meta)
			# save_photo(paddr_url, photo_dir, '%s_%s_%s_%s.jpg' % (str(landmark_index).zfill(3), str(photo_index).zfill(3), paddr.replace(',', '_'), paddr_bearing), f_meta)

			download_zoom_photo(paddr, paddr_bearing, photo_index, landmark_index)
			photo_index += 1

		# ===== End of google =====

		# ===== Begin of foursquare =====
		# place_id
		place_id = f.readline().rstrip()
		# origin landmark lat-lng (no use for fetching photo ...)
		f.readline()
		# origin landmark paddr (no use for fetching photo ...)
		f.readline()

		# foursquare caddr
		for i in range(5):
			caddr = f.readline().rstrip()
			caddr_bearing = f.readline().rstrip()
			# caddr_url = generate_url(caddr, query_fov, caddr_bearing, query_key_google)

			# # prevent sever error...
			# time.sleep(sleep_time)
			# # save_photo(caddr_url, photo_dir, '%s_%s_foursquare_caddr_%s.jpg' % (str(landmark_index).zfill(3), place_id, str(i).zfill(3)), f_meta)
			# save_photo(caddr_url, photo_dir, '%s_%s_%s_%s.jpg' % (str(landmark_index).zfill(3), str(photo_index).zfill(3), caddr.replace(',', '_'), caddr_bearing), f_meta)

			download_zoom_photo(caddr, caddr_bearing, photo_index, landmark_index)
			photo_index += 1

		# foursquare paddr
		for i in range(5):
			paddr = f.readline().rstrip()
			paddr_bearing = f.readline().rstrip()
			# paddr_url = generate_url(paddr, query_fov, paddr_bearing, query_key_google)

			# # prevent sever error...
			# time.sleep(sleep_time)
			# # save_photo(paddr_url, photo_dir, '%s_%s_foursquare_paddr_%s.jpg' % (str(landmark_index).zfill(3), place_id, str(i).zfill(3)), f_meta)
			# save_photo(paddr_url, photo_dir, '%s_%s_%s_%s.jpg' % (str(landmark_index).zfill(3), str(photo_index).zfill(3), paddr.replace(',', '_'), paddr_bearing), f_meta)

			download_zoom_photo(paddr, paddr_bearing, photo_index, landmark_index)
			photo_index += 1

		# ===== End of foursquare =====

		landmark_index += 1