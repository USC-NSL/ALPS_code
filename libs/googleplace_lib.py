import urllib2
import json
import os

# query_key_google = 'AIzaSyAdtMHxfsESr0OuVdGuseM_VW_uiDtahJY'
query_key_google = open(os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/config/query_key_google.info').readline().rstrip()	# ex. AIzaSyAdtMHxfsESr0OuVdGuseM_VW_uiDtahJY

# encode address, location, etc.
# because url request with ' ' or '#' will make error...
def encodeString(inputString):
	outputString = str(inputString).replace(' ', '%20').replace('#', '%23')
	return outputString

# printing error message: input is missing
def input_error_message(function_name, variable_name):
	return 'Error: auto_landmark_lib/%s: %s is none...' % (function_name, variable_name)

# opening the required url, and printing corresponding metadata
def execute_url(function_name, url):
	print '=== googleplace_lib/%s ===' % function_name
	print url
	
	# Send the GET request to the Place details service (using url from above)
	response = urllib2.urlopen(url)

	# Get the response and use the JSON library to decode the JSON
	json_raw = response.read()
	json_data = json.loads(json_raw)

	if json_data['status'] != 'OK':
		print 'Error: auto_landmark_lib/%s: status is not ok...' % function_name
		return None
	else:
		return json_data

# Query Google Place Geocoding API
# which converts address (like "1600 Amphitheatre Parkway, Mountain View, CA") into geographic coordinates (like latitude 37.423021 and longitude -122.083739)
# Sample Query
# https://maps.googleapis.com/maps/api/geocode/json?address=ca%2090007&key=AIzaSyAdtMHxfsESr0OuVdGuseM_VW_uiDtahJY
# Details at https://developers.google.com/maps/documentation/geocoding/
def googleplace_geocoding(address, key = query_key_google):
	if (address is None):
		print input_error_message('googleplace_geocoding', 'address')
		return None
	else:
		addressString = encodeString(address)

		# Compose a URL to query google place geocoding
		url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s') % (addressString, key)
		json_data = execute_url('googleplace_geocoding', url)

		return json_data

# Query Google Place Radar API
# which allows you to search for up to 200 places around your point of interest (POI) with target name of place, lat-lng and radius
# Sample Query
# https://maps.googleapis.com/maps/api/place/radarsearch/json?location=34.0230117,%20-118.2793114&radius=10000&key=AIzaSyAdtMHxfsESr0OuVdGuseM_VW_uiDtahJY&name=subway
# Details at https://developers.google.com/places/webservice/search#RadarSearchRequests
def googleplace_radar(name, lat = 34.0295114, lng = -118.2848199, radius = 10000, key = query_key_google):
	if (name is None):
		print input_error_message('googleplace_radar', 'name')
		return None
	else:
		nameString = encodeString(name)
		latString = str(lat)
		lngString = str(lng)
		radiusString = str(radius)

		# Compose a URL to query google place radar
		url = ('https://maps.googleapis.com/maps/api/place/radarsearch/json?location=%s,%s&radius=%s&key=%s&name=%s') % (latString, lngString, radiusString, key, nameString)
		json_data = execute_url('googleplace_radar', url)

		return json_data

# Query Google Place Nearby API
# which allows you to search place near a point of interest
# Sample Query
# 
# Details at https://developers.google.com/places/web-service/search#PlaceSearchRequests
def googleplace_nearby(name, lat = 34.0295114, lng = -118.2848199, radius = 200, key = query_key_google):
	if (name is None):
		print input_error_message('googleplace_nearby', 'name')
		return None
	else:
		nameString = encodeString(name)
		latString = str(lat)
		lngString = str(lng)
		radiusString = str(radius)

		# Compose a URL to query google place radar
		url = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s&radius=%s&key=%s&name=%s') % (latString, lngString, radiusString, key, nameString)
		json_data = execute_url('googleplace_nearby', url)

		return json_data	

# Query Google Place Place Details API
# Input: placeid from the output of Google Place Search
# Output: place details in json...
# Sample Query
# https://maps.googleapis.com/maps/api/place/details/json?placeid=ChIJVwcybwnIwoAR8y-bT8MtX4w&key=AIzaSyAdtMHxfsESr0OuVdGuseM_VW_uiDtahJY
# Details at https://developers.google.com/places/webservice/details
def googleplace_placedetails(place_id, key = query_key_google):
	if (place_id is None):
		print input_error_message('googleplace_placedetails', 'place_id')
		return None
	else:
		placeidString = str(place_id)

		# Compose a URL to query google place details
		url = ('https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=%s') % (placeidString, key)
		json_data = execute_url('googleplace_placedetails', url)

		return json_data

# Query Google Place Directions API
# Input's origin and destination should be String. Ex: '38.1,-118' or '1234 W 21th St'
# Sample Query
# https://maps.googleapis.com/maps/api/directions/json?origin=34.023149,%20-118.279594&destination=34.023149,%20-118.279594&key=AIzaSyAdtMHxfsESr0OuVdGuseM_VW_uiDtahJY
# Details at https://developers.google.com/maps/documentation/directions/
def googleplace_directions(origin, destination, key = query_key_google):
	if (origin is None) or (destination is None):
		print input_error_message('googleplace_directions', 'origin or destination')
		return None
	else:
		originString = str(origin)
		destinationString = str(destination)

		# Compose a URL to query google place directions
		url = ('https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&key=%s') % (originString, destinationString, key)
		json_data = execute_url('googleplace_directions', url)

		return json_data

def calibrate_parse(json_data):
	if (json_data is not None):
		for tmp1 in json_data['routes']:
			for tmp2 in tmp1['legs']:
				roadLat = float(tmp2['start_location']['lat'])
				roadLng = float(tmp2['start_location']['lng'])	

		return roadLat, roadLng	

def calibrate_paddr(paddr, key = query_key_google):
	if (paddr is None):
		print input_error_message('calibrate_paddr', 'paddr')
		return None
	else:
		paddrString = encodeString(str(paddr))
		json_data = googleplace_directions(paddrString, paddrString, key)

		return calibrate_parse(json_data)

def calibrate_caddr(lat, lng, key = query_key_google):
	if (lat is None) or (lng is None):
		print input_error_message('calibrate_caddr', 'lat or lng')
		return None
	else:
		caddrString = str(lat) + ',' + str(lng)
		json_data = googleplace_directions(caddrString, caddrString, key)

		return calibrate_parse(json_data)


