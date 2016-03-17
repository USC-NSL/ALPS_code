




# ====== main =====
if __name__ == '__main__':

	query_city = open("./config/query_city.info", "r").readline().rstrip()
	work_dir = "./data/%s/" % query_city


	f1 = open(work_dir + "fov_confidence_level_output.txt", "r")
	f2 = open(work_dir + "LA_fov.txt", "r")

	d = dict()

	f1_len = 2640
	f2_len = 1080

	for i in range(f1_len / 2):
		tmp = f1.readline().rstrip()
		d[tmp] = 0
		f1.readline()

	for i in range(f2_len / 2):
		tmp = f2.readline().rstrip()
		d[tmp] += 1
		f2.readline()

	f1.close()

	f1 = open(work_dir + "fov_confidence_level_output.txt", "r")
	for i in range(f1_len/12):
		tmp1 = f1.readline().rstrip()
		f1.readline()
		tmp2 = f1.readline().rstrip()
		f1.readline()
		tmp3 = f1.readline().rstrip()
		f1.readline()
		tmp4 = f1.readline().rstrip()
		f1.readline()
		tmp5 = f1.readline().rstrip()
		f1.readline()
		tmp6 = f1.readline().rstrip()
		f1.readline()

		print "%s %d %d %d %d %d %d" % (tmp1[:-4].ljust(100), d[tmp1], d[tmp2], d[tmp3], d[tmp4], d[tmp5], d[tmp6])