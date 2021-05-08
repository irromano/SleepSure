
import sys
import numpy as np
import os
import pickle
import pandas as pd
import statistics
from scipy import stats
#reads a file in and comes up with an array
def innerQuartileRange(dataset):
     # Interquartile range (IQR)
    iqr = stats.iqr(dataset, interpolation = 'midpoint')
    #print(iqr)
    average=abs(statistics.median(dataset))
    if(average<=0):
        average=1
    return [iqr/average]
#calculates stdv of array and divides by mean
def stdvCalculator(array):
    standard_dev=statistics.stdev(array)
    average=abs(statistics.median(array))
    print(average)
    if(average<=0):
        average=1
    return [standard_dev/ average]
#calculates range and divides by mean
def rangeCalculator(array):
    range=max(array)-min(array)
    average=abs(statistics.median(array))
    if(average<=0):
        average=1
    return [range/average]
#absvalue mean
def absValueMean(array):
    sum=0
    for num in array:
        sum+=abs(num)
    average=abs(statistics.median(array))
    if(average<=0):
        average=1
    return [sum/4096/average]
#reads file and comes up with an array
def readFile(filename):
    testing =open(filename)
    testing=testing.read().split('\n')
    testing.pop()
    testing=np.array(testing)
    testing=list(map(int, testing))
    return testing
#opens the model
def open_model(filename):
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model
#creates dataframe from array
def arrayMaker(array):
    
    stdv=stdvCalculator(array)
    rangeCalc=rangeCalculator(array)
    iqr=innerQuartileRange(array)
    absVal=absValueMean(array)
    df=pd.DataFrame()
    df['Standard Deviation']=stdv
    df['Range']=rangeCalc
    df['Inner Quartile Range']=iqr
    #df['Absolute Value Mean']= absVal
    print(df)
    return (df)
#returns accuarcy of data
def accuracyChecker(classificationArray, actual_classification):
    amountRight=0
    for classification in classificationArray:
        if classification==actual_classification:
            amountRight+=1
    return amountRight/len(classificationArray)
#tests a given path
def tester(modelPath, filename):
    catArray=["Non Seizure","Seizure"]
    model=open_model(modelPath)
    testingArray=readFile(filename)
    df=arrayMaker(testingArray)
    prediction=(int)(model.predict(df))
    print(catArray[prediction])
    return catArray[prediction]
#tests a folder
def folderTester(modelpath,filepath):
    num=0
    classifierArray=[]
    for subdir, dirs, files in os.walk(filepath):
        for file in files:
            print("Number: "+str(num)+": "+filepath )
            filename= (os.path.join(subdir, file))
            classification=tester(modelpath, filename)
            classifierArray.append(classification)
            num+=1
    return classifierArray
#passing in the path as a system argument
path=sys.argv[1]
print(path)
classified_array=folderTester("finalized_model.sav",path )
print(accuracyChecker(classified_array, "Non Seizure"))
#tester("finalized_model.sav", r"C:\Users\Nathan Joseph\Desktop\OpenBCI_GUI\data\EEG_Sample_Data\Meditation\Meditation 1.txt", "Non Selzure")