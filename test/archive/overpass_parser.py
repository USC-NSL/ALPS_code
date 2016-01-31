import json
import utm
import math

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

# computer the theta angle between two point,
# origin and destination, both of which are in lat-lng
# input: origin and destination in lat-lng
# output: theta in angle
# about atan2
#   - east -> 0
#   - west -> 180/-180
#   - north -> 90
#   - south -> -90
# def get_theta3(origin, destination):
# 	# convert origin from lat-lng to xy
# 	xy = utm.from_latlon(origin.lat, origin.lng)
# 	originXY = point(float(xy[0]), float(xy[1]))
# 	# convert destination from lat-lng to xy
# 	xy = utm.from_latlon(destination.lat, destination.lng)
# 	destinationXY = point(float(xy[0]), float(xy[1]))

# 	theta = math.atan2(destinationXY.y - originXY.y, destinationXY.x - originXY.x) * 180 / math.pi
# 	return theta

# def get_theta2(origin, destination):
# 	theta = (destination.lat - origin.lat) / (destination.lng - origin.lng)
# 	return theta

def get_theta(origin, destination):
	theta = math.atan2(destination.lat - origin.lat, destination.lng - origin.lng) * 180 / math.pi
	return theta

def generate_seven(node0, theta):
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

# def generate_seven2(node0, theta):
# 	intersection_id = node0.id
# 	standing_array = []
# 	for i in range(1, 8):
# 		move_length = 0.0001 * i
# 		# delta_lat = move_length * math.sin(theta * math.pi / 180)
# 		# delta_lng = move_length * math.cos(theta * math.pi / 180)
# 		delta_lat = move_length * (theta / math.sqrt(1 + theta * theta))
# 		delta_lng = move_length * (1 / math.sqrt(1 + theta * theta))

# 		#currently, we don't use googleplace_lib.calibrate_caddr
# 		lat = node0.lat + delta_lat
# 		lng = node0.lng + delta_lng
# 		standing_array.append(node(intersection_id, lat, lng))

# 	return standing_array

# ====== main =====
if __name__ == '__main__':

	overpass_input = open("./overpass_input.json", "r")
	json_data = json.loads(overpass_input.read())

	if (json_data is None):
		print "Error!"
	else:
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
				node_id_list = [str(i) for i in element["nodes"]]
				way_hmap[id] = way(id, node_id_list)

		intersection_id = "63068643"
		for id, tmpnode in node_hmap.items():
			if (tmpnode.id == intersection_id):
				node0 = tmpnode
		# print "intersection node0=%s, (%s, %s)" % (node0.id, node0.lat, node0.lng)

		for id, tmpway in way_hmap.items():
			# print "\tway id=%s:" % id
			for i in range(len(tmpway.node_id_list)):
				if (tmpway.node_id_list[i] == intersection_id):
					# print "\ttwo adjacent node with id %s and %s" % (tmpway.node_id_list[i - 1], way.node_id_list[i + 1])
					node1_id = tmpway.node_id_list[i - 1]
					node2_id = tmpway.node_id_list[i + 1]
					node1 = node_hmap[node1_id]
					node2 = node_hmap[node2_id]
			# print "\t\tadjacent node1=%s, (%s, %s)" % (node1.id, node1.lat, node1.lng)
			# print "\t\tadjacent node2=%s, (%s, %s)" % (node2.id, node2.lat, node2.lng)

			theta1 = get_theta(node0, node1);
			# print theta1
			theta2 = get_theta(node0, node2);
			# print theta2

			#now we will generate 8 standing points
			#(one intersection point and seven standing points along the road segment)
			#all this node will be assign node_id=intersection_id
			standing_array1 = generate_seven(node0, theta1)
			print "%s, %s" % (node1.lat, node1.lng)
			print "%s, %s" % (node2.lat, node2.lng)

			for i in standing_array1:
				print "%s, %s" % (i.lat, i.lng)


			standing_array2 = generate_seven(node0, theta2)
			for i in standing_array2:
				print "%s, %s" % (i.lat, i.lng)