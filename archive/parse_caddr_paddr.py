query_name = open('./config/query_name.info').readline().rstrip()		# ex. subway
query_zip = open('./config/query_zip.info').readline().rstrip()			# ex. CA 90007
# query_zip = 'MA02138'

f = open('./data/%s/%s/generate_seed_location_meta.txt' % (query_name, query_zip), 'r')

caddr = []
paddr = []

num = 0

# for i in range(num):
while(f.readline()):
	f.readline()
	tmp = f.readline().rstrip()
	caddr.append(tmp)
	tmp = f.readline().rstrip()
	paddr.append(tmp)
	f.readline()
	f.readline()
	f.readline()

	num += 1

for i in range(num):
	print caddr[i]

for i in range(num):
	print paddr[i]