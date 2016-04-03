file_dir = "data_for_fig/"

file_name = "Google_combined.txt"

f_input = open(file_dir + file_name, "r").readlines()

output = ""

for i in range(len(f_input) - 1):
	tmp = f_input[i].rstrip()
	output += tmp + ", "

output += f_input[len(f_input) - 1].rstrip()

print output