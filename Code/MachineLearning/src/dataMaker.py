import os
def createSets(location):
    setName=[[]]
    for subdir, dirs, files in os.walk(location):
        for file in files:
            
            filename= (os.path.join(subdir, file))
            eeg_signal=open(filename)
            subBands=eeg_signal.read().split('\n')
            subBands.pop()
            for i in range(0, len(subBands)):
                subBands[i]=int(subBands[i])
            setName.append(subBands)
    setName.pop(0)
    return (setName)
array=createSets(r"C:\Users\Nathan Joseph\Desktop\OpenBCI_GUI\data\EEG_Sample_Data\Meditation\meditation.csv")
print(len(array))