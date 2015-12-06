from libs import googleplace_lib
from libs import foursquare_lib

import os

# point in lat-lng plane, with optional place_id
class landmark():
	def __init__(self, lat, lng, place_id = None, address = None):
		self.place_id = place_id
		self.lat = float(lat)
		self.lng = float(lng)
		self.address = address

def generate_seed_location_array(query_name, query_zip, query_radius):

	# query Google Place Geocoding API to convert Zip Code to a point in lat-lng
	# then we will use this point as center to find landmarks nearby
	json_data_geocoding = googleplace_lib.googleplace_geocoding(query_zip)
	if (json_data_geocoding is None):
		return None, None, False
	else:
		for place in json_data_geocoding['results']:
			query_lat = place['geometry']['location']['lat']
			query_lng = place['geometry']['location']['lng']

		# query Google Place Radar API to get lists of the landmark (ex. subway, chase bank, etc.) near the point
		json_data_radar = googleplace_lib.googleplace_radar(query_name, query_lat, query_lng, query_radius)
		if (json_data_radar is None):
			return None, None, False
		else:
			landmark_array_google = []
			landmark_array_foursquare = []

			# for test/debugging only...
			test_index = 0

			for place in json_data_radar['results']:

				test_index += 1
				# let's play with the first seed location first...
				if (test_index > 1000):
					break

				place_lat_google = float(place['geometry']['location']['lat'])
				place_lng_google = float(place['geometry']['location']['lng'])
				place_id_google = place['place_id']		

				# begin to query foursquare to find another pair of lat-lng
				# we set radius for foursquare as "50", because we believe that
				# data from google and foursquare should be no larger than 50 meters
				json_data_revenues = foursquare_lib.foursquare_venues_search(query_name, place_lat_google, place_lng_google, "50")
				if (json_data_revenues is not None):

					# we use f_index to index the number of landmark that
					# foursquare takes as near to landmark from GooglePlace
					# if f_index is not equal to 1, then there is something wrong...
					f_index = 0

					for place in json_data_revenues['response']['venues']:

						f_index += 1

						place_lat_foursquare = float(place['location']['lat'])
						place_lng_foursquare = float(place['location']['lng'])
						place_id_foursquare = place['id']
						
						# Note: there are some query result, which has multi return results, doesn't have ['location']['address']
						# Ex: https://api.foursquare.com/v2/venues/search?ll=34.055974,-118.236052&oauth_token=EDGOAYNIA10AOGX0S4BPMEJMKHBOCVRTIFU3TVVVHESNLPJC&v=20150601&radius=50&query=subway
						# !!! and ['location']['address'] only contains road information, doesn't include city information
						if ('address' in place['location']):
							if ('formattedAddress' in place['location']):
								# place_address_foursquare = ''
								tmp = place['location']['formattedAddress']
								place_address_foursquare = '%s, %s' % (str(place['location']['address']), str(tmp[1]))
							else:
								place_address_foursquare = '...'
						else:
							place_address_foursquare = '...'

					if (f_index == 1 and place_address_foursquare != '...'):
						json_data_place_details = googleplace_lib.googleplace_placedetails(place_id_google)
						if (json_data_place_details is not None):
							place_address_google = json_data_place_details['result']['formatted_address']

							landmark_array_google.append(landmark(place_lat_google, place_lng_google, place_id_google, place_address_google))
							landmark_array_foursquare.append(landmark(place_lat_foursquare, place_lng_foursquare, place_id_foursquare, place_address_foursquare))

			return landmark_array_google, landmark_array_foursquare, True

# ====== main =====
if __name__ == '__main__':

	query_name = open('./config/query_name.info').readline().rstrip()		# ex. subway
	query_zip = open('./config/query_zip.info').readline().rstrip()			# ex. CA 90007
	query_radius = open('./config/query_radius.info').readline().rstrip()	# ex. 10000

	work_dir = './data/%s/%s/' % (query_name, query_zip)
	if not os.path.exists(work_dir):
		os.makedirs(work_dir)

	f_meta = open(work_dir + 'generate_seed_location_meta.txt', 'w')

	landmark_array_google, landmark_array_foursquare, ok = generate_seed_location_array(query_name, query_zip, query_radius)
	if (not ok):
		f_meta.write('Error: in generate_seed_location_array...\n')
	else:
		for index in range(len(landmark_array_google)):

			print(index)

			f_meta.write('----------\n')
			f_meta.write('%s\n' % landmark_array_google[index].place_id)
			f_meta.write('%f,%f\n' % (landmark_array_google[index].lat, landmark_array_google[index].lng))
			f_meta.write('%s\n' % landmark_array_google[index].address)

			f_meta.write('%s\n' % landmark_array_foursquare[index].place_id)
			f_meta.write('%f,%f\n' % (landmark_array_foursquare[index].lat, landmark_array_foursquare[index].lng))
			f_meta.write('%s\n' % landmark_array_foursquare[index].address)

	f_meta.close()