from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np
import pickle
class kMeans():
    def __init__(self):
        print("Running K Means")
    
    def graph(self, coefArray):
        print()
    #generates probability distributin of subband
    def probStatistic(self, outputArray):
        distribution=[]
        class1=0
        class2=0
        class3=0
        class4=0
        class5=0
        class6=0
        total=len(outputArray)
        for output in outputArray:
            if(output==0):
                class1+=1
            elif (output==1):
                class2+=1
            elif(output==2):
                class3+=1
            elif(output==3):
                class4+=1
            elif(output==4):
                class5+=1
            else:
                class6+=1
        distribution.append(class1/total)
        distribution.append(class2/total)
        distribution.append(class3/total)
        distribution.append(class4/total)
        distribution.append(class5/total)
        distribution.append(class6/total)
        return distribution
    #runs kMean
    def runModel(self, coefArray, size, dwtName):
        print("Running Model")
        clustering=KMeans(n_clusters=6, random_state=5)
        distributionArray=[]
        clustering.fit(np.array(coefArray).reshape(-1,1))
        if(dwtName==0):
            pickle.dump(clustering, open("A2.pckl", "wb"))
        elif(dwtName==1):
             pickle.dump(clustering, open("D2.pckl", "wb"))
        else:
            pickle.dump(clustering, open("D1.pckl", "wb"))
        clusters=clustering.cluster_centers_
        subbands=(int)(len(coefArray)/size)
        for i in range(0,subbands):
                distributionArray.append(self.probStatistic(clustering.predict(np.array(coefArray[i*62:(i+1)*62]).reshape(-1,1))))
        return (distributionArray)
    #runs kmean for testing
    def runModelTest(self, coefArray, size, name):
        print("Running Model")
        distributionArray=[]
        clustering=pickle.load(open(name, "rb"))
        clustering.fit(np.array(coefArray).reshape(-1,1))
        subbands=(int)(len(coefArray)/size)
        for i in range(0,subbands):
                distributionArray.append(self.probStatistic(clustering.predict(np.array(coefArray[i*62:(i+1)*62]).reshape(-1,1))))
        return (distributionArray)
  