# Victor Zhang, August 6, 2018
# Plotter for Socket Data (Temperature)
# Python

import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd

## Variables
fileName = 'tempData.dat'
color = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '0.5'] # 0.5 is a gray color
step = 1 # step when reading array (lowest can be 1)
channelNames = {1:'PT2 Head', 2:'PT2 Plate', 3:'1 K Plate', 4:'Still', 5:'mK Plate Cernox', 6:'PT1 Head', 7:'PT1 Plate', 8:'mK Plate RuOx'}
firstTime = ""
count = 0

## Plotting
allData = pd.read_csv(fileName)
print(len(allData['Time'].values))
firstTime = allData['Time'].values[0]
print("This is firstTime: %s" % firstTime)


plt.figure(figsize=(12,8))
for i in range(0,8):
	plt.plot(list(j for j in range(0,len(allData['Time'].values))),allData[str(i+1)].values[::step].astype(np.float),color[i])
plt.legend(list('Chl. ' + str(i+1) for i in range(0, 8)),loc='upper right')
plt.gcf().autofmt_xdate() # beautify the x-labels
plt.gcf().subplots_adjust(bottom=0.15)
plt.title('Temperature of Channels vs. Time')
plt.xlabel('Date and Time')
plt.ylabel('Temperature (K)')
plt.tight_layout()



for i in range(0,1): # should be range(0, 8), but not successfully tested with 8, since my computer heats up
	fig = plt.figure(figsize=(12,8))
	#plt.plot(allData[str(i+1)].values[::step].astype(np.float))
	plt.plot(allData[str(i+1)].values[::step].astype(np.float))
	plt.xticks(range(len(allData[str(i+1)])),allData['Time'].values)

	ax = plt.gca() # get the current axis (which axis you get is determined by the methods used with ax)
	for label in ax.get_xticklabels():
		label.set_visible(False)
		ax.xaxis.get_ticklines()[count].set_visible(False)
		print("Just set %s to invisible" % count)

		if next((value for value in allData['Time'].values[0:count] if allData['Time'].values[count][:10] == value[:10]), None) == None:
			label.set_visible(True)
			ax.xaxis.get_ticklines()[count].set_visible(True)
			print("Hi")
		else:
			pass

		count += 1

	plt.gcf().autofmt_xdate()
	plt.gcf().subplots_adjust(bottom=0.25)
	plt.title(channelNames[i+1] + ', (Channel ' + str(i+1) + '), Temperature vs. Time')
	plt.xlabel('Date and Time')
	plt.ylabel('Temperature (K)')
	plt.tight_layout()
	count = 0

plt.show()
