import matplotlib.pyplot as plt
import numpy as np
import csv
from itertools import islice
import pandas as pd

allData = np.array(list(str(i) for i in range(0,9)))
print("This is allData")
print(allData)
tempData = np.array(9)
color = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '0.5'] # 0.5 is a gray color
skip = 0 # how many rows to skip over
test = np.array(9)


allData=np.loadtxt(open('tempData.dat','r'),dtype='object',delimiter=',',)
print("This is allData")
#print(allData[1:2,2:3])
#allData = np.asarray(allData)
print(allData)
print(allData[:,:1])

allData = pd.read_csv('tempData.dat')
print(allData['Time'].values)
'''
for i in range(0,9):
	plt.plot(allData[:,:1][i][0], int(allData[:,i+1:i+2][]), colors[i])
# beautify the x-labels
plt.gcf().autofmt_xdate()

plt.show()
'''
for i in range(0,8):
	plt.plot(allData['Time'].values,allData[str(i+1)].values.astype(np.float),color[i])
plt.legend(('Ch. 1', 'Ch. 2', 'Ch. 3', 'Ch. 4', 'Ch. 5', 'Ch. 6', 'Ch. 7', 'Ch. 8'),
           loc='upper right')
plt.gcf().autofmt_xdate()
plt.show()
