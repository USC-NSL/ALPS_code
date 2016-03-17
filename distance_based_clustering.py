import math



query_city = open("./config/query_city.info", "r").readline().rstrip()
work_dir = "./data/%s/" % query_city

f_input = open(work_dir + "07-mtv_48.txt", "r")
f_output = open(work_dir + "distance_based_clustering_output.txt", "w")


class node():
	def __init__(self, lat, lng, theta = 0):
		self.lat = float(lat)
		self.lng = float(lng)
		self.theta = float(theta)

def calculate_distance_in_degree(origin, destination):
	delta_lat = origin.lat - destination.lat
	delta_lng = origin.lng - destination.lng

	result = math.sqrt(delta_lat * delta_lat + delta_lng * delta_lng)

	return result

# ====== main =====
if __name__ == '__main__':

	image_number = 48
	min_radius = 0.0005

	node_dict = dict()

	for i in range(image_number):
		tmp = f_input.readline().rstrip().split(',')
		view_lat = tmp[0]
		view_lng = tmp[1]
		node_dict[i] = node(view_lat, view_lng)



	while (len(node_dict) != 0):

		center_node = node(node_dict[node_dict.keys()[0]].lat, node_dict[node_dict.keys()[0]].lng)

		is_stable = False
		in_cluster_array = []
		old_cluster_len = 0

		while (not is_stable):
			for key, value in node_dict.items():
				distance = calculate_distance_in_degree(center_node, value)
				if (distance <= min_radius):
					in_cluster_array.append(node(value.lat, value.lng))
					del node_dict[key]

			new_cluster_len = len(in_cluster_array)

			sum_lat = 0
			sum_lng = 0
			for i in range(new_cluster_len):
				sum_lat += in_cluster_array[i].lat
				sum_lng += in_cluster_array[i].lng

			center_node = node(sum_lat/new_cluster_len, sum_lng/new_cluster_len)

			if (new_cluster_len == old_cluster_len):
				is_stable = True

			old_cluster_len = new_cluster_len

		# print "=== result ==="
		# print new_cluster_len
		print "%s,%s" % (center_node.lat, center_node.lng)