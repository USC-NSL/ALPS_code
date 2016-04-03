import numpy as np
import os,sys
import matplotlib.pyplot as plt

X_LIM = 30
LINE_WIDTH = 3
FONT_SIZE = 17
X_LABLE = 'error(m)'
Y_LABLE = 'CDF'
TITLE = 'Distribution of errors (MTV)'

color_list = ['g', 'r']

legend_list = ['ALPS','Google']

for i in range(1,len(sys.argv)):
	data = np.loadtxt(sys.argv[i])
	sorted_data = np.sort(data)
	yvals=np.arange(len(sorted_data))/float(len(sorted_data))
	print yvals
	print '------------'
	if sorted_data[-1] < X_LIM:
		yvals[-1] = 1.0
	plt.plot(sorted_data,yvals,lw=LINE_WIDTH,color=color_list[i-1])
	if sorted_data[-1] < X_LIM:
		plt.plot([sorted_data[-1], X_LIM], [0.995, 0.995], color=color_list[i-1], lw=LINE_WIDTH)

plt.legend(legend_list, loc=4)
ltext = plt.gca().get_legend().get_texts()
for i in range(1,len(sys.argv)):
	plt.setp(ltext[i-1], color=color_list[i-1])

plt.title(TITLE)
plt.xlim([0, X_LIM])
plt.ylim([0,1.0])
plt.xlabel(X_LABLE, fontsize=FONT_SIZE)
plt.ylabel(Y_LABLE, fontsize=FONT_SIZE)
plt.xticks(fontsize=FONT_SIZE)
plt.yticks(fontsize=FONT_SIZE)

plt.show()
