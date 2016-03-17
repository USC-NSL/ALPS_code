import glob

# ====== main =====
if __name__ == '__main__':

	f_query_city = open("./config/query_city.info", "r")
	query_city = f_query_city.readline().rstrip()
	query_state = f_query_city.readline().rstrip()

	work_dir = "./data/%s/" % query_city

	# ===============================================================================
	file_name = "LA_87.txt"
	# ===============================================================================

	f_input = open(work_dir + file_name, "r").readlines()

	for i in range(len(f_input)):
		tmp = f_input[i].rstrip().split('/')[-1][:-4].split('_')
		print "%s,%s" % (tmp[4], tmp[5])