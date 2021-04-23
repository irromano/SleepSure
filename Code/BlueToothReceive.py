# Receives data from bluetooth over COM3
# Author: Matias Saavedra Silva
import serial
import time

count = 0
filename = "data"
fileNum = 0
file = open(filename+str(fileNum)+".txt", "w")
fileLength = 1024 # Max entries in a file

s = serial.Serial("COM3", 115200) # timeout?
print("Listening on " + s.portstr)
while(1):
    time.sleep(.02)
    recv = s.readline()[:-1].decode() # Remove newline character
    if len(recv) > 0:
        #print(recv)
        file.write(str(recv)+'\n')
        count = count + 1
        # When file is full close and create next data file
        if count == fileLength:
        	file.close()
        	if fileNum == 7:
        		break
        	fileNum = fileNum + 1
        	file = open(filename+str(fileNum)+".txt", "w")
        	count = 0
    if recv == "exit":
        break
