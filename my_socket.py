import socket
from datetime import datetime
import time
#import numpy as np

## Variables
ip_address = "192.168.0.12"
brght = 1 # 0=25%, 1=50%, 2=75%, 3=100%
returnData = ""
date_time = ""
allTemp = ""
count = 0
sleepTime = 60 # how many seconds between temperature taking
#allData = np.array(list(i for i in range(0,9)))
#print("This is allData:")
#print(allData)
#tempData = np.zeros(9)

## Constants
rdgst_dict = {"000":"Valid reading is present", "001":"CS OVL", "002":"VCM OVL", "004":"VMIX OVL", "008":"VDIF OVL", "016":"R. OVER", "032":"R. UNDER", "064":"T. OVER", "128":"T. UNDER"}
term = "\r\n"

## Data file
file = open("tempData.dat", "w")


## Starting socket communication and data acquisition
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_hostname = socket.gethostname()
localfqdn = socket.getfqdn()
server_address = (ip_address, 7777)
sock.connect(server_address)
print("Connecting to %s at Port %s" % server_address)

sock.send("*IDN?" + term)
data = sock.recv(1024)
print("Identification: ")
if data:
    print("%s"% data)
else:
    print("no more data")
    print("-------------\n")

sock.send("NETID?" + term)
data = sock.recv(1024)
print("Network Configuration: ")
if data:
    print("%s"% data)
else:
    print("no more data")
    print("-------------\n")

print("Changing brightness to %s%%" % str((brght+1)*25))
sock.send("BRIGT " + str(brght) + term)
sock.send("BRIGT?" + term)
data = sock.recv(1024)
if data:
    print("Brightness is set to: %s%%" % str((int(data)+1)*25))
else:
    print("no more data")
    print("-------------\n")

print("Checking for errors (0 for none, 1 for errors found):")
sock.send("*TST?" + term)
data = sock.recv(1024)
if data:
    print("%s"% data)
else:
    print("no more data")
    print("-------------\n")

print("Time,1,2,3,4,5,6,7,8,")
file.write("Time,1,2,3,4,5,6,7,8\n")

## Starting the data acquisition

while True:
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print date_time
    allTemp = date_time + ","
    #tempData[0] = date_time


    print("Status and Reading of Thermometers:")
    for i in range(0,8):
        command = "RDGST? " + str(i+1) + term
        sock.send(command)
        data = sock.recv(1024)[:-2]
        if data:
            pass
        #    print("Channel %s: %s " % (str(i+1),rdgst_dict[data]))
        #    print("(bit weighting: %s)" % data)
        else:
            print("Error at Channel %s (RDGST? command)" % str(i+1))
            print("-------------\n")
        
        command2 = "RDGK? " + str(i+1) + term # interestingly, there is another Kelvin Reading Query: KRDG?, see manual
        sock.send(command2)
        data = sock.recv(1024)[:-2]
        allTemp += data +","
        #tempData[i+1] = data
        #print(float(data))
        if data:
            pass
        #    print("Temperature at Channel %s: %s\n"% (str(i+1),data))
        else:
            print("Error at Channel %s (RDGK? command)" % str(i+1))
            print("-------------\n")
    print(allTemp +"\n")
    file.write(allTemp + "\n")
#    allData = 
    #count+=1
    time.sleep(sleepTime) # sleeps/waits for specified time, before taking data again

    #if datetime.now().strftime('%Y-%m-%d')=='2018-08-03':
    #    break
    if datetime.now().strftime('%Y-%m-%d')=='2018-08-06' and int(datetime.now().strftime('%Y-%m-%d %H:%M:%S')[11:13])==10:
        print("YES, ending")
        break
sock.close()
file.close()

