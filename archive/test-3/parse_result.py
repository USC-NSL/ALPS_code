f = open('./triangulation_output.txt', 'r')
# f = open('./data/%s/%s/do_triangulation_for_logo_detection_ground_truth_meta.txt' % (query_name, query_zip), 'r')

detected_num = []
system_result = []

num = 0

while (f.readline()):
	tmp = f.readline().rstrip().split(' ')
	detected_num.append(tmp[1])
	tmp = f.readline().rstrip()
	if (tmp[0] == 'H'):
		system_result.append(' ')
	else:
		system_result.append(tmp)

	num += 1

for i in range(num):
	print detected_num[i]

for i in range(num):
	print system_result[i]


