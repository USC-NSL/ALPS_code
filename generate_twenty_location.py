from libs import googleplace_lib
from libs import foursquare_lib

import math
import utm

# point in lat-lng plane, with optional place_id
class landmark():
	def __init__(self, lat, lng, place_id = None, address = None, caddr = None, paddr = None):
		self.place_id = place_id
		self.lat = float(lat)
		self.lng = float(lng)
		self.address = address

		self.caddr = caddr
		self.paddr = paddr

class easymark():
	def __init__(self, lat, lng, bearing):
		self.lat = float(lat)
		self.lng = float(lng)
		self.bearing = bearing

# point in x-y plane
class point():
	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)


def read_array_from_generate_four_location_meta(work_dir):

	f = open(work_dir + 'generate_four_location_meta.txt', 'r')

	landmark_array_google = []
	landmark_array_foursquare = []

	while (f.readline()):
		place_id_google = f.readline().rstrip()
		tmp = f.readline().rstrip().split(',')
		place_lat_google = tmp[0]
		place_lng_google = tmp[1]
		place_address_google = f.readline().rstrip()

		tmp = f.readline().rstrip().split(',')
		tmp2 = f.readline().rstrip()
		place_caddr_google = easymark(tmp[0], tmp[1], tmp2)

		tmp = f.readline().rstrip().split(',')
		tmp2 = f.readline().rstrip()
		place_paddr_google = easymark(tmp[0], tmp[1], tmp2)

		place_id_foursquare = f.readline().rstrip()
		tmp = f.readline().rstrip().split(',')
		place_lat_foursquare = tmp[0]
		place_lng_foursquare = tmp[1]
		place_address_foursquare = f.readline().rstrip()

		tmp = f.readline().rstrip().split(',')
		tmp2 = f.readline().rstrip()
		place_caddr_foursquare = easymark(tmp[0], tmp[1], tmp2)

		tmp = f.readline().rstrip().split(',')
		tmp2 = f.readline().rstrip()
		place_paddr_foursquare = easymark(tmp[0], tmp[1], tmp2)

		landmark_array_google.append(landmark(place_lat_google, place_lng_google, place_id_google, place_address_google, place_caddr_google, place_paddr_google))
		landmark_array_foursquare.append(landmark(place_lat_foursquare, place_lng_foursquare, place_id_foursquare, place_address_foursquare, place_caddr_foursquare, place_paddr_foursquare))

		# to get ride of the gf_distance...
		f.readline()

	return landmark_array_google, landmark_array_foursquare

# inverse the effect of calibrate_bearing()
# namely, get it back to the result of get_theta()...
#   - east -> 0
#   - west -> 180/-180
#   - north -> 90
#   - south -> -90
def inverse_calibrate_bearing(bearing):
	theta = 90 - float(bearing)
	return theta

# computer the theta angle between two point,
# origin and destination, both of which are in lat-lng
# input: origin and destination in lat-lng
# output: theta in angle
# about atan2
#   - east -> 0
#   - west -> 180/-180
#   - north -> 90
#   - south -> -90
def get_theta(origin, destination):
	# convert origin from lat-lng to xy
	xy = utm.from_latlon(origin.lat, origin.lng)
	originXY = point(float(xy[0]), float(xy[1]))
	# convert destination from lat-lng to xy
	xy = utm.from_latlon(destination.lat, destination.lng)
	destinationXY = point(float(xy[0]), float(xy[1]))

	theta = math.atan2(destinationXY.y - originXY.y, destinationXY.x - originXY.x) * 180 / math.pi
	return theta

# about theta
#   - east -> 90
#   - west -> 270/-90
#   - north -> 0
#   - south -> 180
def calibrate_bearing(theta):
	if theta < 270:
		bearing = 90 - theta
	else:
		bearing = 450 - theta

	return bearing

def generate_five(my_easymark, destination):
	my_easymark_array = []
	my_easymark_array.append(my_easymark)

	for i in range(-2, 3):
		if (i == 0):
			continue
		else:
			if (i > 0):
				theta = inverse_calibrate_bearing(my_easymark.bearing) + 90
			else:
				theta = inverse_calibrate_bearing(my_easymark.bearing) - 90
				
			move_length = 0.0001 * abs(i)

			delta_lat = move_length * math.sin(math.pi * theta / 180)
			delta_lng = move_length * math.cos(math.pi * theta / 180)

			tmp_lat = my_easymark.lat + delta_lat
			tmp_lng = my_easymark.lng + delta_lng

			new_lat, new_lng = googleplace_lib.calibrate_caddr(tmp_lat, tmp_lng)
			tmp_landmark = landmark(new_lat, new_lng)

			addr_theta = get_theta(tmp_landmark, destination)
			addr_bearing = calibrate_bearing(addr_theta)

			tmp_easymark = easymark(new_lat, new_lng, addr_bearing)

			my_easymark_array.append(tmp_easymark)

	return my_easymark_array


# ====== main =====
if __name__ == '__main__':

	query_name = open('./config/query_name.info').readline().rstrip()		# ex. subway
	query_zip = open('./config/query_zip.info').readline().rstrip()			# ex. CA 90007
	
	work_dir = './data/%s/%s/' % (query_name, query_zip)
	landmark_array_google, landmark_array_foursquare = read_array_from_generate_four_location_meta(work_dir)

	f_meta = open(work_dir + 'generate_twenty_location_meta.txt', 'w')

	for index in range(len(landmark_array_google)):
		# again, for test usage only...
		# print landmark_array_google[index].lat, landmark_array_google[index].lng
		# print landmark_array_google[index].address
		# print landmark_array_google[index].caddr.lat, landmark_array_google[index].caddr.lng
		# print landmark_array_google[index].caddr.bearing

		print index

		f_meta.write('----------\n')

		# ===== Start of landmark_array_google =====
		f_meta.write('%s\n' % landmark_array_google[index].place_id)
		f_meta.write('%f,%f\n' % (landmark_array_google[index].lat, landmark_array_google[index].lng))
		f_meta.write('%s\n' % landmark_array_google[index].address)

		# for g_caddr
		g_caddr_array = generate_five(landmark_array_google[index].caddr, landmark_array_google[index])
		# record five point: 0, 1, 2, -1, -2
		for i in range(5):
			f_meta.write('%f,%f\n' % (g_caddr_array[i].lat, g_caddr_array[i].lng))
			f_meta.write('%s\n' % g_caddr_array[i].bearing)

		# for g_paddr
		g_paddr_array = generate_five(landmark_array_google[index].paddr, landmark_array_google[index])
		# record five point: 0, 1, 2, -1, -2
		for i in range(5):
			f_meta.write('%f,%f\n' % (g_paddr_array[i].lat, g_paddr_array[i].lng))
			f_meta.write('%s\n' % g_paddr_array[i].bearing)

		# ===== End of landmark_array_google =====

		# ===== Start of landmark_array_foursquare =====
		f_meta.write('%s\n' % landmark_array_foursquare[index].place_id)
		f_meta.write('%f,%f\n' % (landmark_array_foursquare[index].lat, landmark_array_foursquare[index].lng))
		f_meta.write('%s\n' % landmark_array_foursquare[index].address)

		# for f_caddr
		f_caddr_array = generate_five(landmark_array_foursquare[index].caddr, landmark_array_foursquare[index])
		# record five point: 0, 1, 2, -1, -2
		for i in range(5):
			f_meta.write('%f,%f\n' % (f_caddr_array[i].lat, f_caddr_array[i].lng))
			f_meta.write('%s\n' % f_caddr_array[i].bearing)

		# for f_paddr
		f_paddr_array = generate_five(landmark_array_foursquare[index].paddr, landmark_array_foursquare[index])
		# record five point: 0, 1, 2, -1, -2
		for i in range(5):
			f_meta.write('%f,%f\n' % (f_paddr_array[i].lat, f_paddr_array[i].lng))
			f_meta.write('%s\n' % f_paddr_array[i].bearing)

		# ===== End of landmark_array_foursquare =====


