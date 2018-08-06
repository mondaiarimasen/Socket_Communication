# Victor Zhang, August 6, 2018
# Temperature Acquisition from Lake Shore 372 device
# Python
import socket
from datetime import datetime
import time

## Variables
ip_address = "192.168.0.12"
brght = 1 # 0=25%, 1=50%, 2=75%, 3=100%
date_time = ""
allTemp = ""
sleepTime = 60 # how many seconds between temperature taking
stopDate = "2018-08-06" # write in %Y-%m-%d format
stopHour = 10 # what hour (in 24 hours) want to stop; ex. if want to stop at 10:00, then stopHour = 10

## Constants
rdgst_dict = {"000":"Valid reading is present", "001":"CS OVL", "002":"VCM OVL", "004":"VMIX OVL", "008":"VDIF OVL", "016":"R. OVER", "032":"R. UNDER", "064":"T. OVER", "128":"T. UNDER"}
term = "\r\n"

## Data file
fileName = 'tempData.dat'

## Starting socket communication
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_hostname = socket.gethostname()
localfqdn = socket.getfqdn()
server_address = (ip_address, 7777)
sock.connect(server_address)
print("Connecting to %s at Port %s" % server_address)

# Identification query; gives: LSCI,MODEL372,LSA2245,1.3
sock.send("*IDN?" + term)
data = sock.recv(1024)
print("Identification: ")
if data:
    print("%s"% data)
else:
    print("no more data")
    print("-------------\n")

# Network Configuration query
sock.send("NETID?" + term)
data = sock.recv(1024)
print("Network Configuration: ")
if data:
    print("%s"% data)
else:
    print("no more data")
    print("-------------\n")

# Brightness
print("Changing brightness to %s%%" % str((brght+1)*25))
sock.send("BRIGT " + str(brght) + term)
sock.send("BRIGT?" + term)
data = sock.recv(1024)
if data:
    print("Brightness is set to: %s%%" % str((int(data)+1)*25))
else:
    print("no more data")
    print("-------------\n")

# Self-Test query
print("Checking for errors (0 for none, 1 for errors found):")
sock.send("*TST?" + term)
data = sock.recv(1024)
if data:
    print("%s"% data)
else:
    print("no more data")
    print("-------------\n")

## Starting the data acquisition
fileName = 'tempData.dat'
file = open(fileName, 'w')
print("Time,1,2,3,4,5,6,7,8,")
file.write("Time,1,2,3,4,5,6,7,8,\n")

while True:
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print date_time
    allTemp = date_time + ","

    print("Status and Reading of Thermometers:")
    for i in range(0,8):
        command = "RDGST? " + str(i+1) + term
        sock.send(command)
        data = sock.recv(1024)[:-2]
        if data:
            pass
        else:
            print("Error at Channel %s (RDGST? command)" % str(i+1))
            print("-------------\n")

        command2 = "RDGK? " + str(i+1) + term # interestingly, there is another Kelvin Reading Query: KRDG?, see manual
        sock.send(command2)
        data = sock.recv(1024)[:-2]
        allTemp += data +","
        if data:
            pass
        else:
            print("Error at Channel %s (RDGK? command)" % str(i+1))
            print("-------------\n")
    print(allTemp +"\n")
    file.write(allTemp + "\n")
    time.sleep(sleepTime) # sleeps/waits for specified time, before taking data again

    # stops the data taking at 10:00 on Aug. 6, 2018; ran this code over weekend
    # from 20:40 on Aug. 3 to 10:00 on Aug. 6. 2018
    if date_time[:10]==stopDate and int(date_time[11:13])==stopHour:
        print("YES, ending")
        break
sock.close()
file.close()
