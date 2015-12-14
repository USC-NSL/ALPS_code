
f = open('./data/subway/CA94035/generate_seed_location_meta.txt', 'r')

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