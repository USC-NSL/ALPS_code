import glob

# ====== main =====
if __name__ == '__main__':

	query_city = open("./config/query_city.info", "r").readline().rstrip()
	work_dir = "./data/%s/" % query_city

	# image_dir = work_dir + "confidence_level_with_different_zoom/"

	# format = image_dir + "*.jpg"

	# for image_path in sorted(glob.glob(format)):
	# 	print image_path.split('/')[-1][:-4]	

	# f_input = open(work_dir + "zoom_conf.txt", "r")
	# a = []
	# for i in range(280):
	# 	tmp = f_input.readline().rstrip()
	# 	a.append(tmp)
	# 	tmp = f_input.readline().rstrip()

	# a = sorted(a)

	# for i in range(280):
	# 	print a[i][:-4]





	# f1 = open("output1.txt", "r")
	# f2 = open("output2.txt", "r")

	# d = dict()

	# for i in range(510):
	# 	tmp = f1.readline().rstrip()
	# 	d[tmp] = 0

	# for i in range(280):
	# 	tmp = f2.readline().rstrip()
	# 	d[tmp] += 1

	# f1.close()

	# f1 = open("output1.txt", "r")
	# for i in range(510 / 6):
	# 	tmp1 = f1.readline().rstrip()
	# 	# print tmp[:-4]
	# 	# print "\t%d" % d[tmp]

	# 	tmp2 = f1.readline().rstrip()
	# 	# print "\t%d" % d[tmp]
	# 	tmp3 = f1.readline().rstrip()
	# 	# print "\t%d" % d[tmp]
	# 	tmp4 = f1.readline().rstrip()
	# 	# print "\t%d" % d[tmp]
	# 	tmp5 = f1.readline().rstrip()
	# 	# print "\t%d" % d[tmp]
	# 	tmp6 = f1.readline().rstrip()
	# 	# print "\t%d" % d[tmp]

	# 	print "%s %d %d %d %d %d %d" % (tmp1[:-4].ljust(100), d[tmp1], d[tmp2], d[tmp3], d[tmp4], d[tmp5], d[tmp6])



	f = open("./output4.txt", "r")
	for i in range(48):
		tmp = f.readline().rstrip().split('_')
		print "%s,%s" % (tmp[4], tmp[5])


