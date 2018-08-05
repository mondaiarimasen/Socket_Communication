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

## Plotting
allData = pd.read_csv(fileName)

plt.figure(figsize=(12,8))
for i in range(0,8):
	plt.plot(allData['Time'].values,allData[str(i+1)].values[::step].astype(np.float),color[i])
plt.legend(list('Chl. ' + str(i+1) for i in range(0, 8)),loc='upper right')
plt.gcf().autofmt_xdate() # beautify the x-labels
plt.gcf().subplots_adjust(bottom=0.15)
plt.title('Temperature of Channels vs. Time')
plt.xlabel('Date and Time')
plt.ylabel('Temperature (K)')

for i in range(0,8):
	plt.figure(figsize=(12,8))
	plt.plot(allData['Time'].values,allData[str(i+1)].values[::step].astype(np.float),color[i])
	plt.gcf().autofmt_xdate()
	plt.gcf().subplots_adjust(bottom=0.25)
	plt.title(channelNames[i+1] + ', (Channel ' + str(i+1) + '), Temperature vs. Time')
	plt.xlabel('Date and Time')
	plt.ylabel('Temperature (K)')

plt.show()
