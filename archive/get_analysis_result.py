import utm
import math

# the following two classes and one function come from generate_four_location.py

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

# ====== main =====
if __name__ == '__main__':

	query_name = open('./config/query_name.info').readline().rstrip()

	flag = raw_input('Run without zoom? (y/n): ')
	if (flag == 'y'):
		query_name = query_name
	else:
		query_name = '%s_with_merge' % query_name


	f_seed = open('./data/%s/generate_seed_location_meta.txt' % query_name, 'r')
	f_system_result = open('./data/%s/do_triangulation_meta.txt' % query_name, 'r')
	f_xiaochen_eye_gt = open('./data/%s/xiaochen_eye_gt.txt' % query_name, 'r')

	f_output_seed_latlng = open('./data/%s/get_combine_seed_and_system_result_output_seed_latlng.txt' % query_name, 'w')
	f_output_paddr = open('./data/%s/get_combine_seed_and_system_result_output_paddr.txt' % query_name, 'w')
	f_output_num_detected_photo = open('./data/%s/get_combine_seed_and_system_result_output_num_detected_photo.txt' % query_name, 'w')
	f_output_system_result = open('./data/%s/get_combine_seed_and_system_result_output_system_result.txt' % query_name, 'w')
	f_output_eye_gt = open('./data/%s/get_combine_seed_and_system_result_output_eye_gt.txt' % query_name, 'w')
	f_output_distance = open('./data/%s/get_combine_seed_and_system_result_output_distance.txt' % query_name, 'w')


	# f_output = open('./data/%s/get_analysis_result_output.txt')

	landmark_index = 0

	while (f_seed.readline()):
		# f_output.write('=== play with the %dth landmark ===\n' % landmark_index)
		print landmark_index

		# deal with f_seed
		f_seed.readline() # read google_id

		seed_latlng = f_seed.readline().rstrip()
		f_output_seed_latlng.write('%s\n' % seed_latlng)

		seed_paddr = f_seed.readline().rstrip()
		f_output_paddr.write('%s\n' % seed_paddr)

		f_seed.readline() # read foursquare_id
		f_seed.readline() # read foursquare_caddr
		f_seed.readline() # read foursquare_paddr

		# deal with f_system_result
		f_system_result.readline()
		num_detected_photo = f_system_result.readline().rstrip().split(' ')[1]
		f_output_num_detected_photo.write('%s\n' % num_detected_photo)
		system_result_latlng = f_system_result.readline().rstrip()
		if (system_result_latlng[0] == 'H'):
			f_output_system_result.write('0,0\n')

			eye_gt = f_xiaochen_eye_gt.readline().rstrip()
			f_output_eye_gt.write('%s\n' % eye_gt)

			f_output_distance.write('None\n')
		else:
			f_output_system_result.write('%s\n' % system_result_latlng)

			eye_gt = f_xiaochen_eye_gt.readline().rstrip()
			f_output_eye_gt.write('%s\n' % eye_gt)

			tmp = system_result_latlng.split(',')
			origin = landmark(tmp[0], tmp[1])
			tmp = eye_gt.split(',')
			destination = landmark(tmp[0], tmp[1])

			if (destination.lat < 1): # this means destination = (0, 0) error...
				f_output_distance.write('None\n')
			else:
				distance = get_distance(origin, destination)
				f_output_distance.write('%s\n' % str(distance))


		landmark_index += 1
