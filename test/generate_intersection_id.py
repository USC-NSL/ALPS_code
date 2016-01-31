import urllib2
import json
import os


# opening the required url, and printing corresponding metadata
def execute_url(function_name, url):
	print '=== overpass_lib/%s ===' % function_name
	print url
	
	# Send the GET request to the Place details service (using url from above)
	response = urllib2.urlopen(url)

	# Get the response and use the JSON library to decode the JSON
	json_raw = response.read()
	json_data = json.loads(json_raw)

	return json_data

# def bbox(self, lat_min, lng_min, lat_max, lng_max):
# 	self.lat_min = lat_min
# 	self.lng_min = lng_min
# 	self.lat_max = lat_max
# 	self.lng_max = lng_max

# ====== main =====
if __name__ == '__main__':

	f_output = open("./data/generate_intersection_id_output.txt", "w")

	my_bbox = "34.021738,-118.280490,34.023119,-118.278977"

	query = "[out:json];node[\"highway\"~\"traffic_signals|stop\"](%s);out;" % my_bbox
	url = "http://overpass-api.de/api/interpreter?data=%s" % query

	json_data = execute_url("main", url)

	if (json_data is None):
		print "Error!"
	else:
		# print "Good!"
		for element in json_data["elements"]:
			if (element["type"] == "node"):
				f_output.write("%s\n" % str(element["id"]))



