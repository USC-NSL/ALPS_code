import json
import utm
import math
import urllib2

# opening the required url, and printing corresponding metadata
def execute_url(function_name, url):
	# print '=== overpass_lib/%s ===' % function_name
	# print url
	
	# Send the GET request to the Place details service (using url from above)
	response = urllib2.urlopen(url)

	# Get the response and use the JSON library to decode the JSON
	json_raw = response.read()
	json_data = json.loads(json_raw)

	return json_data

class node():
	def __init__(self, id, lat, lng):
		self.id = str(id)
		self.lat = float(lat)
		self.lng = float(lng)

class way():
	def __init__(self, id, node_id_list):
		self.id = str(id)
		self.node_id_list = [str(i) for i in node_id_list]

# point in x-y plane
class point():
	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)

def get_theta(origin, destination):
	theta = math.atan2(destination.lat - origin.lat, destination.lng - origin.lng) * 180 / math.pi
	return theta

def generate_seven(node0, node1):
	theta = get_theta(node0, node1)

	intersection_id = node0.id
	standing_array = []
	for i in range(1, 8):
		move_length = 0.0001 * i
		delta_lat = move_length * math.sin(theta * math.pi / 180)
		delta_lng = move_length * math.cos(theta * math.pi / 180)

		#currently, we don't use googleplace_lib.calibrate_caddr
		lat = node0.lat + delta_lat
		lng = node0.lng + delta_lng
		standing_array.append(node(intersection_id, lat, lng))

	return standing_array

# ====== main =====
if __name__ == '__main__':

	node_id_array = []
	# with open("./generate_intersection_id_output.txt", "r") as f_input:
	# 	node_id = f_input.readline().rstrip()
	# 	node_id_array.append(node_id)

	f_input = open("./data/generate_intersection_id_output.txt", "r")
	f_output = open("./data/generate_standing_point_output.txt", "w")
	for i in range(2):
		node_id = f_input.readline().rstrip()
		node_id_array.append(node_id)

	# print len(node_id_array)
	for node_id_index in range(len(node_id_array)):
		intersection_id = node_id_array[node_id_index]

		# query = "[out:json];node(%s);way(around._:20)[highway~\"primary|secondary|residential\"];(._;>;);out;" % intersection_id
		query = "[out:json];node(%s);way(around._:5)[highway];(._;>;);out;" % intersection_id
		url = "http://overpass-api.de/api/interpreter?data=%s" % query

		json_data = execute_url("main", url)

		if (json_data is None):
			print "Error!"
		else:
			# print "Good!"
			node_hmap = {}
			way_hmap = {}
			for element in json_data["elements"]:
				if (element["type"] == "node"):
					# print element["id"]
					id = str(element["id"])
					lat = str(element["lat"])
					lng = str(element["lon"])
					node_hmap[id] = node(id, lat, lng)
				elif (element["type"] == "way"):
					# print element["id"]
					id = str(element["id"])
					node_id_list = [str(tmp) for tmp in element["nodes"]]
					way_hmap[id] = way(id, node_id_list)

			for id, tmpnode in node_hmap.items():
				if (tmpnode.id == intersection_id):
					node0 = tmpnode

			standing_array_result = []
			standing_array_result.append(node0)

			node_on_ways = 0
			for id, tmpway in way_hmap.items():
				for i in range(len(tmpway.node_id_list)):
					if (tmpway.node_id_list[i] == intersection_id):
						# node_on_ways += 1
						if (i == 0):
							node_on_ways += 1

							node2_id = tmpway.node_id_list[i + 1]
							node2 = node_hmap[node2_id]
							# node1_lat = 2 * node0.lat - node2.lat
							# node1_lng = 2 * node0.lng - node2.lng
							# node1 = node(0, node1_lat, node1_lng)
							# standing_array1 = generate_seven(node0, node1)
							# standing_array_result.extend(standing_array1)
							standing_array2 = generate_seven(node0, node2)
							standing_array_result.extend(standing_array2)

						elif (i == (len(tmpway.node_id_list) - 1)):
							node_on_ways += 1

							node1_id = tmpway.node_id_list[i - 1]
							node1 = node_hmap[node1_id]
							# node2_lat = 2 * node0.lat - node1.lat
							# node2_lng = 2 * node0.lng - node1.lng
							# node2 = node(0, node2_lat, node2_lng)
							standing_array1 = generate_seven(node0, node1)
							standing_array_result.extend(standing_array1)
							# standing_array2 = generate_seven(node0, node2)
							# standing_array_result.extend(standing_array2)

						else:
							node_on_ways += 2

							node1_id = tmpway.node_id_list[i - 1]
							node2_id = tmpway.node_id_list[i + 1]
							node1 = node_hmap[node1_id]
							node2 = node_hmap[node2_id]

							standing_array1 = generate_seven(node0, node1)
							standing_array_result.extend(standing_array1)
							standing_array2 = generate_seven(node0, node2)
							standing_array_result.extend(standing_array2)



				# print "%s,%s" % (node1.lat, node1.lng)
				# print "%s,%s" % (node2.lat, node2.lng)

				# theta1 = get_theta(node0, node1);
				# theta2 = get_theta(node0, node2);

				# standing_array1 = generate_seven(node0, theta1)
				# for i in standing_array1:
				# 	print "%s,%s" % (i.lat, i.lng)


				# standing_array2 = generate_seven(node0, theta2)
				# for i in standing_array2:
				# 	print "%s,%s" % (i.lat, i.lng)
			# if (node_on_ways == 2):
			# print node_on_ways
			f_output.write("=== play with the %dth intersection ===\n" % node_id_index)
			f_output.write("%s\n" % node0.id)
			f_output.write("%s,%s\n" % (node0.lat, node0.lng))

			f_output.write("%d\n" % node_on_ways)
			for i in range(node_on_ways):
				node3 = standing_array_result[1 + i * 7]
				theta = get_theta(node0, node3) + 90
				f_output.write("%s\n" % str(theta))
				f_output.write("%s,%s\n" % (node3.lat, node3.lng))
				for j in range(6):
					node4 = standing_array_result[2 + i * 7 + j]
					f_output.write("%s,%s\n" % (node4.lat, node4.lng))

			# for i in range(len(standing_array_result)):
			# 	print "%s,%s" % (standing_array_result[i].lat, standing_array_result[i].lng)








