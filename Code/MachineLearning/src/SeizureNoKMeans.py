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
import cv2


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
def turn_df_to_array(df):
    return df.to_numpy()
#function to create the probability distributions based on training and tresting
def create_prob_functions(DWT):
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

    #creating coeffecients
    
    testA_coeffs=DWT.getCoeffecients(setA)
    testB_coeffs=DWT.getCoeffecients(setB)
    testC_coeffs=DWT.getCoeffecients(setC)
    testD_coeffs=DWT.getCoeffecients(setD)
    testE_coeffs=DWT.getCoeffecients(setE) 


   
    approximate_coeff=[]

    outputSet=[0]*400 +[1]*100 
    #creating the rows in dataframe
    for setLen in range(0,100):
        #approximate
        approximate_coeff.append(testA_coeffs[setLen][0])
        approximate_coeff.append(testB_coeffs[setLen][0])
        approximate_coeff.append(testC_coeffs[setLen][0])
        approximate_coeff.append(testD_coeffs[setLen][0])
        approximate_coeff.append(testE_coeffs[setLen][0])

        #d2
        """
        d2coef.append(testA_coeffs[setLen][1])
        d2coef.append(testB_coeffs[setLen][1])
        d2coef.append(testC_coeffs[setLen][1])
        d2coef.append(testD_coeffs[setLen][1])
        d2coef.append(testE_coeffs[setLen][1])
        #d3
        d1coef.append(testA_coeffs[setLen][2])
        d1coef.append(testB_coeffs[setLen][2])
        d1coef.append(testC_coeffs[setLen][2])
        d1coef.append(testD_coeffs[setLen][2])
        d1coef.append(testE_coeffs[setLen][2])
        """
    total_df=pd.DataFrame(data=approximate_coeff)
    #total_df['Approximate']=approgitximate_coeff
    #total_df['D2']=d2coef
    #total_df['D1']=d1coef
    total_df['Output']=outputSet
    #total_df=total_df.sample(frac=1).reset_index(drop=True)
    #cprint(total_df)
    return total_df
DWT=DWT.DWT()
prob_functions= create_prob_functions(DWT)
cnn=CNN.CNN()
#cnn.graph(prob_functions, 'Approximate', 0 )
#cnn.graph(prob_functions, 'D2', 0 )
#cnn.graph(prob_functions, 'D1', 0 )

#breaking it up into seizure and on seizure
seizure=prob_functions.tail(100)
seizure=seizure.sample(frac=1).reset_index(drop=True)

non_seizure=prob_functions.head(400)
non_seizure=non_seizure.sample(frac=1).reset_index(drop=True)

training_frames=[non_seizure.head(200), seizure.head(100)]
training_input = pd.concat(training_frames)

testing_frames=[non_seizure.tail(100), seizure.tail(100)]
testing_input = pd.concat(testing_frames)
#getting rid of output in input data 

#output
training_output=training_input['Output']
testing_output=testing_input['Output']
training_output=(turn_df_to_array(training_output))
testing_output=(turn_df_to_array(testing_output))
#input
training_input=training_input.drop(columns=['Output'])
testing_input=testing_input.drop(columns=['Output'])
training_input=(turn_df_to_array(training_input))
testing_input=(turn_df_to_array(testing_input))

print()
print((len(training_input[0])))
cnn.runModel(training_input, testing_input, training_output, testing_output)