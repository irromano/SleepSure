
import sys
import numpy as np
import pywt
import CNN
import os
import pickle
def readFile(filename):
    testing =open(filename)
    testing=testing.read().split('\n')
    testing.pop()
    testing=np.array(testing)
    return testing
def open_model(filename):
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model
def tester(modelPath, filename, actual):
    model=open_model(modelPath)
    testingArray=readFile(filename)
    prediction=model.predict(testingArray)
    print(prediction)
tester("finalized_model.sav", "C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/eyes open/Z001.txt", 1)