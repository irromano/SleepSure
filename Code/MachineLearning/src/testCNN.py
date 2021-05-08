import sys
import numpy as np
import pywt
import CNN
import os
from tkinter.filedialog import askopenfilename
#reads a file and turns it into an array
def readFile():
    #txtFile = askopenfilename()
    testing =open ("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/eyes open/Z001.txt")
    testing=testing.read().split('\n')
    testing.pop()
    testing=np.array(testing)
    return testing
def accuracyTester(location, seizure):
    for subdir, dirs, files in os.walk(location):
        seizureAmount=[]
        for file in files:
            
            filename= (os.path.join(subdir, file))
            eeg_signal=open(filename)
            subBands=eeg_signal.read().split('\n')
            subBands.pop()
            wavelet=dwt(subBands)
            approx=wavelet[0]
            eeg=np.array(subBandTester(approx))
            seizureAmount.append(testBand(eeg,'1'))
  
def dwt(subBand):
    coeffs=pywt.wavedec(subBand, 'db2', level=2)
    
    return coeffs
def subBandTester(approx):
    approx=approx.reshape(1,3,342,1)
    return approx
def testBand(headData, output):
    newModel=CNN.predictModel("my_model.h5", headData)
    #print (newModel)

CNN=CNN.CNN()
#readingi n the file
subBand=readFile()

#DWT
wavelet=dwt(subBand)
approx=wavelet[0]
#getting it into the correct form 
eeg=np.array(subBandTester(approx))
testBand(eeg,'1')
accuracyTester("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/opposite hemisphere", 1)

    

