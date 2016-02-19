import urllib2
import json
import os


# opening the required url, and printing corresponding metadata
def execute_url(function_name, url):
	url = url.replace(' ', '%20')

	print '=== overpass_lib/%s ===' % function_name
	print url
	
	# Send the GET request to the Place details service (using url from above)
	response = urllib2.urlopen(url)

	# Get the response and use the JSON library to decode the JSON
	json_raw = response.read()
	json_data = json.loads(json_raw)

	return json_data


# ====== main =====
if __name__ == '__main__':

	f_output = open("./data/generate_initial_point_output.txt", "w")
	query_city = "Mountain View"

	query = "[out:json];area[name=\"%s\"][\"wikipedia\"=\"en:Mountain View, California\"];way[\"highway\"~\"primary|secondary|tertiary|residential\"](area);out geom;" % query_city
	# query = "[out:json];way(around:20,37.406338, -122.0783056)[\"highway\"~\"primary|secondary\"];out geom;"
	url = "http://overpass-api.de/api/interpreter?data=%s" % query

	json_data = execute_url("main", url)

	if (json_data is None):
		print "Error!"
	else:
		way_index = 0
		for element in json_data["elements"]:
			if (element["type"] == "way"):
				# f_output.write("=== way id %s ===\n" % element["id"])
				f_output.write("=== play with the %dth way ===\n" % way_index)
				f_output.write("%s\n" % element["id"])
				f_output.write("%d\n" % len(element["geometry"]))
				for node in element["geometry"]:
					lat = str(node["lat"])
					lng = str(node["lon"])
					f_output.write("%s,%s\n" % (lat, lng))

				way_index += 1




