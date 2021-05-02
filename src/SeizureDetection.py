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


#creates the set for each category (A-E)
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


#divides each subband into smaller time segments
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

#function to create the probability distributions based on training and tresting
def create_prob_functions(DWT, kMeans):
    #creating the 5 sets of EEG signals
    #eyes open
    rootdir="C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/eyes open"
    setA=createSets(rootdir) 
    #eyes closed
    rootdir="C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/eyes closed"
    setB=createSets(rootdir) 
    #same side as seizure
    rootdir="C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/epileptic hemisphere"
    setC=createSets(rootdir) 
    #opposite side of seizure
    rootdir="C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/opposite hemisphere"
    setD=createSets(rootdir) 
    #actual seizure
    rootdir="C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/Seizure"
    setE=createSets(rootdir) 

    #dividing each subband into 17 parts (each representing around 2 seconds of data)
    test_a=divideArray(setA, 17)
    test_b=divideArray(setB, 17)
    test_c=divideArray(setC, 17)
    test_d=divideArray(setD, 17)
    test_e=divideArray(setE, 17)

  

    #discrete wavelength analysis
    #coeffecients for each set
    #Each set contains 1700 arrays representing each text file
        #Each array contains 3 arrays, representing the Approximate coeffecient, and the two distinct coeffecients
            #Each of those arrays contain the actual decimal coeffecient values 
  
    testA_coeffs=DWT.getCoeffecients(test_a)
    testB_coeffs=DWT.getCoeffecients(test_b)
    testC_coeffs=DWT.getCoeffecients(test_c)
    testD_coeffs=DWT.getCoeffecients(test_d)
    testE_coeffs=DWT.getCoeffecients(test_e)



    #Now I have to pass each sets 3 arrays into a kmeans clustering
        #there will be 3 clustering algorithms, one for the approximate coeffiecent, and two for the distinct two coeffecients
            #From here we will come up with probability distribution
    approximate_coeff=[]
    d2coef=[]
    d1coef=[]


    #walking through the arrays to add to each set
    for i in range(0,1700):
        #approximate for A
        for a in ((testA_coeffs[i][0])):
            approximate_coeff.append(a)
        #d2 for A
        for da2 in ((testA_coeffs[i][1])):
            d2coef.append(da2)
        #d3 for A
        for da1 in ((testA_coeffs[i][2])):
            d1coef.append(da1)
        #approximate for B
        for b in ((testB_coeffs[i][0])):
            approximate_coeff.append(b)
        #d2 for B
        for db2 in ((testB_coeffs[i][1])):
            d2coef.append(db2)
        #d1 for B
        for db1 in ((testB_coeffs[i][2])):
            d1coef.append(db1)
        #approximate for C
        for c in ((testC_coeffs[i][0])):
            approximate_coeff.append(c)
        #d2 for C
        for dc2 in ((testC_coeffs[i][1])):
            d2coef.append(dc2)
        #d1 for C
        for dc1 in ((testC_coeffs[i][2])):
            d1coef.append(dc1)
        #approximate for D
        for d in ((testD_coeffs[i][0])):
            approximate_coeff.append(d)
        #d2 for D
        for dd2 in ((testD_coeffs[i][1])):
            d2coef.append(dd2)
        #d1 for D
        for dd1 in ((testD_coeffs[i][2])):
            d1coef.append(dd1)
        #approximate for E
        for e in ((testE_coeffs[i][0])):
            approximate_coeff.append(e)
        #d2 for E
        for de2 in ((testE_coeffs[i][1])):
            d2coef.append(de2)
        #d1 for E
        for de1 in ((testE_coeffs[i][2])):
            d1coef.append(de1)

   
   #initializing array
    outputSet=[0]*6800+ [1]*1700

    
    #running the probability distributions of each level

    A2distribution=kMeans.runModel(approximate_coeff,62, 0)
    D2distribution=kMeans.runModel(d2coef,62, 1)
    D1distribution=kMeans.runModel(d1coef, 122,2)

    #creating on array with all inputs for MLPNN
    #pre processing
    #Classes A-D (non seizures) are given an output of 0
    #class E (seizure) is given an output of 1
    dataset=pd.DataFrame(np.zeros((8500,18)))
    for subband in range(len(A2distribution)):
        dataset.loc[subband]=((A2distribution[subband] + D2distribution[subband]+ D1distribution[subband]))
    dataset.columns=["A2k1", "A2k2", "A2k3", "K2k4", "A2k5", "A2k6","D2k1", "D2k2", "D2k3", "D2k4", "D2k5", "D2k6","D1k1", "D1k2", "D1k3", "K2k4", "D1k5", "D1k6", ]
    dataset['Output']=outputSet

    #randomizing data
    #dataset=dataset.sample(frac=1).reset_index(drop=True)
    #print (dataset)
    return dataset
    
   

#now that I have the probability distribution I have to pass i,t to a neural network

#creating all of the required things
kMeans=kMeans.kMeans()
DWT=DWT.DWT()
prob_functions= create_prob_functions(DWT, kMeans)
print(prob_functions)
#creating the testing and training data
non_seizure=prob_functions[:6800]
non_seizure=non_seizure.sample(frac=1).reset_index(drop=True)
seizure=prob_functions[6800:]
seizure=seizure.sample(frac=1).reset_index(drop=True)
training_df=pd.concat([non_seizure.head(650),seizure.head(650)])
testing_df=pd.concat([non_seizure.ix[-650:], seizure.ix[-650:]])
#training_df=seizure.ix[-650:]

#running the  MLPNN neural network 
mlpnn=mlpnn.MLPNN()
model=mlpnn.runModel(training_df, testing_df)

#running the CNN model
#cnn=CNN.CNN()
#cnn.runModel(training_df, testing_df)
"""
#random_test=prob_functions.iloc[:100].drop(columns=['Output'])
#mlpnn.predictModel(model,random_test )
"""

#LSTM, RNN, GRU, CNN 
#loading and saving model
#data and save model 
#https://www.tensorflow.org/tutorials/keras/save_and_load 


#testing the model on new data

