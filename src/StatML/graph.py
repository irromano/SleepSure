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
        iqrArray.append(iqr)
    return iqrArray
def varianceCreator(setName):
    setVariance=[]
    for band in setName:
        setVariance.append(abs(np.var(band)/statistics.mean(band)))
    return setVariance
#calculates stdv of array and divides by mean
def stdvCalculator(dataset):
    stdvArray=[]
    for band in dataset:
        standard_dev=statistics.stdev(band)
        stdvArray.append(standard_dev)
    return stdvArray 
#calculates range and divides by mean
def rangeCalculator(dataset):
    rangeArray=[]
    for band in dataset:
        range=max(band)-min(band)
        rangeArray.append(range)
    return rangeArray
def absValueMean(dataset):
    absMean=[]
    for band in dataset:
        sum=0
        for num in band:
            sum+=abs(num)
        absMean.append(sum)
    return absMean
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
    #Basic staistics
    # #variance 
    varA=varianceCreator(setA)
    varB=varianceCreator(setB)
    varC=varianceCreator(setC)
    varD=varianceCreator(setD)
    varE=varianceCreator(setE)
    #stdf
    stdvA=stdvCalculator(setA)
    stdvB=stdvCalculator(setB)
    stdvC=stdvCalculator(setC)
    stdvD=stdvCalculator(setD)
    stdvE=stdvCalculator(setE)
    #range
    rangeA=rangeCalculator(setA)
    rangeB=rangeCalculator(setB)
    rangeC=rangeCalculator(setC)
    rangeD=rangeCalculator(setD)
    rangeE=rangeCalculator(setE)
    #iqr
    iqrA=innerQuartileRange(setA)
    iqrB=innerQuartileRange(setB)
    iqrC=innerQuartileRange(setC)
    iqrD=innerQuartileRange(setD)
    iqrE=innerQuartileRange(setE)

    print(statistics.mean(stdvA))
    print(statistics.mean(stdvE))
    #absolute value sum
    absSumA=absValueMean(setA)
    absSumB=absValueMean(setB)
    absSumC=absValueMean(setC)
    absSumD=absValueMean(setD)
    absSumE=absValueMean(setE)

    
    #putting it into a dataset
    outputSet=[0]*40000 +[1]*10000 
    df=pd.DataFrame()
    df['Variance']=np.repeat((varA+varB+varC+varD+varE),100)
    df['Standard Deviation']=np.repeat((stdvA+stdvB+stdvC+stdvD+stdvE),100)
    df['Range']=np.repeat((rangeA+rangeB+rangeC+rangeD+rangeE),100)
    df['Inner Quartile Range']=np.repeat((iqrA+iqrB+iqrC+iqrD+iqrE),100)
    df['Absolute Value']= np.repeat((absSumA+absSumB+absSumC+absSumD+absSumE),100)
    df['Output']=outputSet
    #df=df.sample(frac=1).reset_index(drop=True)
    return df
    #df = df.append(dict(zip(df.columns, varB)), ignore_index=True)
    
    #print(training_df)

df=create_prob_functions()
#linnearRegression=linnearRegression.LinnearRegression()
#linnearRegression.runModel(df)
"""
kMeans=kMeans.kMeans()
category=kMeans.runModel(df)
df['Category']=category
print(df)
"""


training_df=df.tail(20000)
#testing_df=df.tail(20000)
mlpnn=mlpnn.MLPNN()
model=mlpnn.runModel(training_df, df)
