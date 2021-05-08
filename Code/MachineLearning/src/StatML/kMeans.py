from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import numpy as np
class kMeans:
    def __init__(self):
        print("Running kmeans Network")
    def runModel(self, df):
        clustering=KMeans(init="random", n_clusters=2, random_state=8675309)
        features=df.drop(columns=['Output'])
        labels=df['Output']
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=90210)
        clustering.fit(X_train, y_train)
        # apply the labels
        train_labels = clustering.labels_
        # predict labels on the test set
        test_labels = clustering.predict(X_test)
        print(np.array(y_test))
        print(np.array(test_labels))
        return 
    