from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

import numpy as np
class logisticRegression:
    def __init__(self):
        print("Running logistic regression")
    #returns how similar to arrays are
    def accuracy_checker(self, array1, array2):
        numSame=0
        for num in range(len(array1)):
            if(array1[num]==array2[num]):
                numSame+=1
        return numSame/len(array1)
    #runs logistic regression
    def runModel(self, df):
        features=df.drop(columns=['Output'])
        labels=df['Output']
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=90210)
        logisticRegr=LogisticRegression()
        logisticRegr.fit(X_train, y_train)
        predictions=logisticRegr.predict(X_test)
        print(np.array(predictions))
        print(np.array(y_test))
        print(self.accuracy_checker(np.array(predictions), np.array(y_test)))
        #saving model
        filename = 'finalized_model.sav'
        pickle.dump(logisticRegr, open(filename, 'wb'))
        return logisticRegr