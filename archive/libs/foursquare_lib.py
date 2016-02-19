import urllib2
import json
import os

query_key_foursquare = open(os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/config/query_key_foursquare.info').readline().rstrip()	# ex. EDGOAYNIA10AOGX0S4BPMEJMKHBOCVRTIFU3TVVVHESNLPJC

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
	print '=== foursquare_lib/%s ===' % function_name
	print url
	
	# Send the GET request to the Place details service (using url from above)
	response = urllib2.urlopen(url)

	# Get the response and use the JSON library to decode the JSON
	json_raw = response.read()
	json_data = json.loads(json_raw)

	# if json_data['status'] != 'OK':
	# 	print 'Error: auto_landmark_lib/%s: status is not ok...' % function_name
	# 	return None
	# else:
	return json_data

def foursquare_venues_search(name, lat = 34.0295114, lng = -118.2848199, radius = 50, key = query_key_foursquare):
	if (name is None):
		print input_error_message('foursquare_venues_search', 'name')
		return None
	else:
		nameString = encodeString(name)
		latString = str(lat)
		lngString = str(lng)
		radiusString = str(radius)

		# Compose a URL to query foursquare venues search
		url = ('https://api.foursquare.com/v2/venues/search?ll=%s,%s&oauth_token=%s&v=20150601&radius=%s&query=%s') % (latString, lngString, key, radiusString, nameString)
		json_data = execute_url('foursquare_venues_search', url)

		return json_data




