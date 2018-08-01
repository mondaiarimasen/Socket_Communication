# Victor Zhang, July 31, 2018
# Socket connection to Lake Shore 372 (testing connection)
# Python

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

local_hostname = socket.gethostname()

localfqdn = socket.getfqdn()

# This is the IP address of the Lake Shore Model 372 device (now referred to as LS372)
ip_address = "133.11.164.138" #socket.gethostbyname("")

# The Lake Shore Model 372 device connects to port 7777 (see manual)
server_address = (ip_address, 7777)
sock.connect(server_address)
print("Connecting to %s (%s) at %s" % (local_hostname, localfqdn, ip_address))

# Possible Terminator characters (as they are referred to as in the manual):
# CR: carriage return, returns cursor to beginning of line
# LF or NL: line feed, or new line
sock.send("*IDN?LF")
while True:
    data = sock.recv(64) # Wait for up to 1 kbyte of data to be returned (if fewer bytes returned and the instrument signals message complete, the socket terminates and this data is returned)
    print ("Data:")
    if data:
        # output received data
        print ("%s" % data)
    else:
        # no more data -- quit the loop
        print ("no more data.")
        print ("----------------\n")
        break
sock.send("BEEP 1LF") # Should cause the LS372 to beep
sock.send("*TST?LF") # Self-test: retunrs 0 if no errors, 1 if errors found
while True:
    data = sock.recv(64) # Wait for up to 1 kbyte of data to be returned (if fewer bytes returned and the instrument signals message complete, the socket terminates and this data is returned)
    print ("Data:")
    if data:
        # output received data
        print ("%s" % data)
    else:
        # no more data -- quit the loop
        print ("no more data.")
        print ("----------------\n")
        break

#randomData = [243,45242,32,43,5,2,"SDF","123W","313"]
#for ele in randomData:
#    print("data is: ", str(ele))
#    new_data = str("rand1: %s\n" % ele).encode("utf-8")
#    sock.sendall(new_data)

sock.close()
