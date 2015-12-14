from libs import googleplace_lib
from libs import foursquare_lib

import os
import utm
import math

# point in lat-lng plane, with optional place_id
class landmark():
	def __init__(self, lat, lng, place_id = None, address = None):
		self.place_id = place_id
		self.lat = float(lat)
		self.lng = float(lng)
		self.address = address

# point in x-y plane
class point():
	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)

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

def get_distance(origin, destination):
	# convert origin from lat-lng to xy
	xy = utm.from_latlon(origin.lat, origin.lng)
	originXY = point(float(xy[0]), float(xy[1]))
	# convert destination from lat-lng to xy
	xy = utm.from_latlon(destination.lat, destination.lng)
	destinationXY = point(float(xy[0]), float(xy[1]))

	# distance = math.sqrt(destinationXY.y - originXY.y, destinationXY.x - originXY.x) * 180 / math.pi
	distance = math.sqrt((originXY.x - destinationXY.x) ** 2 + (originXY.y - destinationXY.y) ** 2)
	return distance	

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

def read_array_from_generate_seed_location_meta(work_dir):

	f = open(work_dir + 'generate_seed_location_meta.txt', 'r')

	landmark_array_google = []
	landmark_array_foursquare = []

	while (f.readline()):
		place_id_google = f.readline().rstrip()
		tmp = f.readline().rstrip().split(',')
		place_lat_google = tmp[0]
		place_lng_google = tmp[1]
		place_address_google = f.readline().rstrip()

		place_id_foursquare = f.readline().rstrip()
		tmp = f.readline().rstrip().split(',')
		place_lat_foursquare = tmp[0]
		place_lng_foursquare = tmp[1]
		place_address_foursquare = f.readline().rstrip()		

		landmark_array_google.append(landmark(place_lat_google, place_lng_google, place_id_google, place_address_google))
		landmark_array_foursquare.append(landmark(place_lat_foursquare, place_lng_foursquare, place_id_foursquare, place_address_foursquare))

	return landmark_array_google, landmark_array_foursquare


# ====== main =====
if __name__ == '__main__':

	query_name = open('./config/query_name.info').readline().rstrip()		# ex. subway
	query_zip = open('./config/query_zip.info').readline().rstrip()			# ex. CA 90007

	work_dir = './data/%s/%s/' % (query_name, query_zip)
	landmark_array_google, landmark_array_foursquare = read_array_from_generate_seed_location_meta(work_dir)

	f_meta = open(work_dir + 'generate_four_location_meta.txt', 'w')

	for index in range(len(landmark_array_google)):
		# For test usage only...
		# print landmark_array_google[index].address
		# print landmark_array_foursquare[index].address

		print index

		f_meta.write('----------\n')

		# ===== Start of landmark_array_google =====
		f_meta.write('%s\n' % landmark_array_google[index].place_id)
		f_meta.write('%f,%f\n' % (landmark_array_google[index].lat, landmark_array_google[index].lng))
		f_meta.write('%s\n' % landmark_array_google[index].address)

		# There are two way to get a road point
		# Method I
		# Map landmark coordinator address (lat-lng) to a road point
		caddr_road_lat, caddr_road_lng = googleplace_lib.calibrate_caddr(landmark_array_google[index].lat, landmark_array_google[index].lng)
		caddr_road = landmark(caddr_road_lat, caddr_road_lng)

		caddr_theta = get_theta(caddr_road, landmark_array_google[index])
		caddr_bearing = calibrate_bearing(caddr_theta)

		f_meta.write('%f,%f\n' % (caddr_road.lat, caddr_road.lng))
		f_meta.write('%f\n' % caddr_bearing)

		# Method II
		# Map landmark physical address to a road point
		paddr_road_lat, paddr_road_lng = googleplace_lib.calibrate_paddr(landmark_array_google[index].address)
		paddr_road = landmark(paddr_road_lat, paddr_road_lng)
		
		paddr_theta = get_theta(paddr_road, landmark_array_google[index])
		paddr_bearing = calibrate_bearing(paddr_theta)

		f_meta.write('%f,%f\n' % (paddr_road.lat, paddr_road.lng))
		f_meta.write('%f\n' % paddr_bearing)
		# ===== End of landmark_array_google =====

		# ===== Start of landmark_array_foursquare =====
		f_meta.write('%s\n' % landmark_array_foursquare[index].place_id)
		f_meta.write('%f,%f\n' % (landmark_array_foursquare[index].lat, landmark_array_foursquare[index].lng))
		f_meta.write('%s\n' % landmark_array_foursquare[index].address)

		# Method I
		# Map landmark coordinator address (lat-lng) to a road point
		# Here we still use google's api to calibrate lat-lng from Foursquare!!!
		caddr_road_lat, caddr_road_lng = googleplace_lib.calibrate_caddr(landmark_array_foursquare[index].lat, landmark_array_foursquare[index].lng)
		caddr_road = landmark(caddr_road_lat, caddr_road_lng)

		caddr_theta = get_theta(caddr_road, landmark_array_foursquare[index])
		caddr_bearing = calibrate_bearing(caddr_theta)

		f_meta.write('%f,%f\n' % (caddr_road.lat, caddr_road.lng))
		f_meta.write('%f\n' % caddr_bearing)

		# Method II
		# Map landmark physical address to a road point
		paddr_road_lat, paddr_road_lng = googleplace_lib.calibrate_paddr(landmark_array_foursquare[index].address)
		paddr_road = landmark(paddr_road_lat, paddr_road_lng)

		paddr_theta = get_theta(paddr_road, landmark_array_foursquare[index])
		paddr_bearing = calibrate_bearing(paddr_theta)

		f_meta.write('%f,%f\n' % (paddr_road.lat, paddr_road.lng))
		f_meta.write('%f\n' % paddr_bearing)
		# ===== End of landmark_array_foursquare =====

		# record the distance between google's x-y location and foursquare's x-y location
		# In practice, it is not rare that we have a distance larger than 60 meters...
		gf_distance = get_distance(landmark_array_google[index], landmark_array_foursquare[index])
		if (gf_distance > 60):
			f_meta.write('error: ' + str(gf_distance) + '\n')
		else:
			f_meta.write(str(gf_distance) + '\n')		


	f_meta.close()