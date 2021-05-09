# Receives data from bluetooth over COM port
# Author: Matias Saavedra Silva
import serial
import time
import serial.tools.list_ports

count = 0
filename = "Data/data"
fileNum = 0
offset = 8388608
# Create file for each channel
files = []
for i in range(8):
    files.append(open(filename+"_chan"+str(i)+"_"+str(fileNum)+".txt", "w"))
fileLength = 4096 # Max entries in a file

# Check each COM port associated with Bluetooth devices until the test message is sent
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
            s.write(b"\xff")
        except serial.serialutil.SerialTimeoutException:
            print("Connection Unsuccessful")
            s.close()
            continue
        print("Successfully connected to " + i)
        return s
    print("Failed!")
    exit()

print("SleepSure Receiver")
channels = [0,0,0,0,0,0,0,0] # Data from each channel
s = findCOM()
start = time.time()
while(1):
    # Read 26 bytes of data. Data for each channel is 3 bytes plus 2 bytes to show the end of the packet
    recv=s.read(42)
    # Check that the packet is closed correctly
    if recv[-2:] == b'\xff\xff':
        data = recv[:-2]
    else:
        print("Error! Invalid terminating bytes")
        print(recv)
        break
    for i in range(0, len(data), 5):
        # If the data is one byte it will be padded with 0x0000. 2 bytes of data are padded with just 0x00
        if data[i+1:i+5] == b'\x00' * 4:
            toSave = data[i]
        elif data[i+2:i+5] == b'\x00'*3:
            toSave = int.from_bytes(data[i:i+2], 'big')
        elif data[i+3:i+5] == b'\x00'*2:
            toSave = int.from_bytes(data[i:i+3], 'big')
        elif data[i+4] == 0:
            toSave = int.from_bytes(data[i:i+4], 'big')
        else:
            print("Error! Invalid padding for channel", str(i))
            print(data)
            break
        toSave = toSave - offset
        channels[i//5] = toSave
    if len(data) > 0:
        for num, i in enumerate(channels):
            #print("Channel " + str(num) + ": " + str(i))
            files[num].write(str(i)+'\n')
        count = count + 1
        # When file is full close and create next data file
        if count == fileLength:
            print(time.time()-start)
            start = time.time()
            for i in files:
                i.close()
            if fileNum == 7:
                break
            else:
                fileNum = fileNum + 1
                for i in range(8):
                    files[i] = open(filename+"_chan"+str(i)+"_"+str(fileNum)+".txt", "w")
                count = 0
    if recv == "exit":
        break
