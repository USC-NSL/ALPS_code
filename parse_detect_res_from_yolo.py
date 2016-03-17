import glob

# ====== main =====
if __name__ == '__main__':

	f_query_city = open("./config/query_city.info", "r")
	query_city = f_query_city.readline().rstrip()
	query_state = f_query_city.readline().rstrip()

	work_dir = "./data/%s/" % query_city

	# photo_dir = work_dir + "detect_res/"

	# print photo_dir

	# format = photo_dir + "*.png"

	# for file_name in sorted(glob.glob(format)):
	# 	# print file_name
	# 	tmp = file_name.split('/')[-1][:-4].split('_')
	# 	print "%s,%s" % (tmp[4], tmp[5])

	f_input = work_dir + "LA_part1.txt"
	image_num = 116 / 2

	for i in range(image_num):
		tmp = f_input.readline().rstrip().split('/')[-1][:-4].split('_')
		print "%s,%s" % (tmp[4], tmp[5])
		tmp = f_input.readline()
