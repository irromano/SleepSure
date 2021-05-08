#graphing each set
import matplotlib.pyplot as plt
import os
import numpy  as np
from sklearn.metrics import r2_score
import statistics
from scipy.stats import gaussian_kde
from scipy import stats
import pandas as pd
import mlpnn
import kMeans
import linnearRegression
import logisticRegression   
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
#calculates means of array
def meanCalculator(dataset):
    meanArray=[]
    for band in dataset:
        mean=statistics.mean(band)
        meanArray.append(mean)
    return meanArray 
#calculates median of array
def medianCalculator(dataset):
    medArray=[]
    for band in dataset:
        median=statistics.median(band)
        medArray.append(median)
    return medArray 
#calculates variance and divides by mean
def innerQuartileRange(dataset):
    iqrArray=[]
    for band in dataset:
        # Interquartile range (IQR)
        iqr = stats.iqr(band, interpolation = 'midpoint')
        #print(iqr)
        average=abs(statistics.median(band))
        if(average<=0):
            average=1
        iqrArray.append(iqr/average)
    return iqrArray
#variance of array
def varianceCreator(setName):
    setVariance=[]
    for band in setName:
        average=abs(statistics.median(band))
        if(average<=0):
            average=1
        setVariance.append(abs(np.var(band)/average))
    return setVariance
#calculates stdv of array and divides by mean
def stdvCalculator(dataset):
    stdvArray=[]
    for band in dataset:
        standard_dev=statistics.stdev(band)
        average=abs(statistics.median(band))
        if(average<=0):
            average=1
        stdvArray.append(standard_dev/average)
    return stdvArray 
#calculates range and divides by mean
def rangeCalculator(dataset):
    rangeArray=[]
    for band in dataset:
        range=max(band)-min(band)
        average=abs(statistics.median(band))
        if(average<=1):
            average=1
        rangeArray.append(range/average)
    return rangeArray
#mean of absolute value
def absValueMean(dataset):
    absMean=[]
    for band in dataset:
        sum=0
        average=abs(statistics.median(band))
        if(average==0):
            average=1
        for num in band:
            sum+=abs(num)
        absMean.append(sum/4096/average)
    return absMean
#generates a range
def boxPlotInfro(dataArray):
    minVal=min(dataArray)
    maxVal=max(dataArray)
    return [minVal, maxVal]
#function to create the probability distributions based on training and tresting
def create_prob_functions():
    #creating the 5 sets of EEG signals
    #eyes open
    rootdir="C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/eyes open"
    setA=createSets(rootdir) 
    #array of all the means
   
    #setABox=boxPlotInfro(setAmean)
    #print(setABox)
    #eyes closed
    #rootdir="C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/eyes closed"
    #setB=createSets(rootdir)
    #same side as seizure
    #rootdir="C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/epileptic hemisphere"
    #setC=createSets(rootdir) 
    #opposite side of seizure
    #rootdir="C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/opposite hemisphere"
    #setD=createSets(rootdir) 
    #actual seizure
    #rootdir="C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/Seizure"
    setE=createSets(rootdir)
    #Basic staistics
    # #variance 
    varA=varianceCreator(setA)
    #varB=varianceCreator(setB)
    #varC=varianceCreator(setC)
    #varD=varianceCreator(setD)
    varE=varianceCreator(setE)
    #stdf
    stdvA=stdvCalculator(setA)
    #stdvB=stdvCalculator(setB)
    #stdvC=stdvCalculator(setC)
    #stdvD=stdvCalculator(setD)
    stdvE=stdvCalculator(setE)
    #range
    rangeA=rangeCalculator(setA)
    #rangeB=rangeCalculator(setB)
    #rangeC=rangeCalculator(setC)
    #rangeD=rangeCalculator(setD)
    rangeE=rangeCalculator(setE)
    #iqr
    iqrA=innerQuartileRange(setA)
    #iqrB=innerQuartileRange(setB)
    #iqrC=innerQuartileRange(setC)
    #iqrD=innerQuartileRange(setD)
    iqrE=innerQuartileRange(setE)

    #absolute value sum
    absSumA=absValueMean(setA)
    #absSumB=absValueMean(setB)
    #absSumC=absValueMean(setC)
    #absSumD=absValueMean(setD)
    absSumE=absValueMean(setE)

    
    #putting it into a dataset
    outputSet=[0]*100 +[1]*100
    df=pd.DataFrame()
    #df['Variance']=((varA+varE))
    df['Standard Deviation']=((stdvA+stdvE))
    df['Range']=((rangeA+rangeE))
    df['Inner Quartile Range']=((iqrA+iqrE))
    #df['Absolute Value Mean']= ((absSumA+absSumE))
    df['Output']=outputSet
    df=df.sample(frac=1).reset_index(drop=True)
    print(df)
    return df
    
    
    #print(training_df)

df=create_prob_functions()
#linnearRegression=linnearRegression.LinnearRegression()
#linnearRegression.runModel(df)
#runing logistic regression model
logisticRegression=logisticRegression.logisticRegression()
logisticRegression.runModel(df)
"""
kMeans=kMeans.kMeans()
category=kMeans.runModel(df)

"""


#training_df=df.tail(20000)
#testing_df=df.tail(20000)
"""
mlpnn=mlpnn.MLPNN()
model=mlpnn.runModel(training_df, df)
"""
