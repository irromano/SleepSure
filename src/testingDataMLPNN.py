import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import os
import DWT
import kMeans
import mlpnn
import sys
import CNN
import pickle 
#dividing the array into sets
def divideArray(doubleArray, length):
    bigArray=[]
    counter=0
    for i in (doubleArray):
        counter+=1
        tempArray=np.array(i)
        tempArray=np.split(tempArray,length)
        for j in tempArray:
            bigArray.append(j)
    return bigArray

#preprocessing the data
def pre_process(data):
    #discrete wavelet transform
    wavelets=DWT.getCoeffecients(data)
    #different wavelets
    approximate_coeff=[]
    d2coef=[]
    d1coef=[]
    for i in range(0,17):
        #approximate for A
        for a in ((wavelets[i][0])):
            approximate_coeff.append(a)
        #d2 for A
        for da2 in ((wavelets[i][1])):
            d2coef.append(da2)
        #d3 for A
        for da1 in ((wavelets[i][2])):
            d1coef.append(da1)
 
    #kmeans clustering
    
   
    A2distribution=kMeans.runModelTest(approximate_coeff,62, "A2.pckl")
    D2distribution=kMeans.runModelTest(d2coef,62,"D2.pckl")
    D1distribution=kMeans.runModelTest(d1coef, 122,"D1.pckl")
    #d probability istribution
    dataset=pd.DataFrame(np.zeros((17,18)))
    for subband in range(len(A2distribution)):
        dataset.loc[subband]=((A2distribution[subband] + D2distribution[subband]+ D1distribution[subband]))
    dataset.columns=["A2k1", "A2k2", "A2k3", "K2k4", "A2k5", "A2k6","D2k1", "D2k2", "D2k3", "D2k4", "D2k5", "D2k6","D1k1", "D1k2", "D1k3", "K2k4", "D1k5", "D1k6", ]
    print(dataset)
    return dataset
def testResults(subband, output):
    newDataSet=pre_process(subband)
    newModel=mlpnn.predictModel("my_model.h5", newDataSet)
    if output=='1':
        return newModel/len(subband)
    else:
        return (len(subband)-newModel)/len(subband)
DWT=DWT.DWT()
kMeans=kMeans.kMeans()
mlpnn=mlpnn.MLPNN()

testing =open (r"C:\Users\Nathan Joseph\Desktop\CPEG498\SortedData\eyes closed\O001.txt")
testing=testing.read().split('\n')
testing.pop()
testing=np.array(testing)
testing=np.split(testing,17)
print(len(testing))
print(testResults(testing, '1'))

