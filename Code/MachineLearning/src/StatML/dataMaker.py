import os
import numpy as np
import pandas as pd
def createSets(location):
    values=[[]]
    df=pd.read_csv(location)
    val_arrays=df['FP2-F4']
    val_arrays=np.array(val_arrays)
    
    for num in range(37):
        values.append(val_arrays[num*4096:(num+1)*4096])
    #print(values)
    return values

def make_txt(doublearray, path):
    counter=0
    for arrayRead in doublearray:
        path=path.replace(".txt", "")
        path=path+str(counter)+".txt" 
        file=open(path, "x")
        print(arrayRead)
        for num in arrayRead:
            file=open(path, "w")
            file.write(num)
            file.close()
            print(num)
        counter+=1
mediation_array=createSets(r"C:\Users\Nathan Joseph\Desktop\OpenBCI_GUI\data\EEG_Sample_Data\Meditation\meditating.csv")
make_txt(mediation_array, r"C:\Users\Nathan Joseph\Desktop\OpenBCI_GUI\data\EEG_Sample_Data\Meditation\meditating")
print(len(mediation_array))