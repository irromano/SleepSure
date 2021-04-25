# Receives data from bluetooth over COM3
# Author: Matias Saavedra Silva
import serial
import time
import serial.tools.list_ports

count = 0
filename = "Data/data"
fileNum = 0
file = open(filename+str(fileNum)+".txt", "w")
fileLength = 100 # Max entries in a file

#s.write(b"File complete!")
def findCOM():
    possiblePorts = []
    comPorts=serial.tools.list_ports.comports()
    for i in comPorts:
        if "Standard Serial over Bluetooth link" in i.description:
            possiblePorts.append(i.name)
    for i in possiblePorts:
        s = serial.Serial(i, 115200, timeout=1, write_timeout=1) # timeout?
        print("Listening on " + s.portstr)
        try:
            s.write(b"Hello!")
        except serial.serialutil.SerialTimeoutException:
            print("Connection Unsuccessful")
            s.close()
            continue
        print("Successfully connected to " + i)
        return s
    print("Failed!")
    exit()

print("SleepSure Receiver")
s = findCOM()
start = time.time()
while(1):
    time.sleep(.02)
    recv = s.readline()[:-1].decode() # Remove newline character
    if len(recv) > 0:
        #print(recv)
        file.write(str(recv)+'\n')
        count = count + 1
        # When file is full close and create next data file
        if count == fileLength:
            print(time.time()-start)
            start = time.time()
            file.close()
            if fileNum == 7:
                break
            else:
                fileNum = fileNum + 1
                file = open(filename+str(fileNum)+".txt", "w")
                count = 0
    if recv == "exit":
        break
