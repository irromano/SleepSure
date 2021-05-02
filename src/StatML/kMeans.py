from sklearn.cluster import KMeans
import numpy as np
class kMeans:
    def __init__(self):
        print("Running kmeans Network")
    def runModel(self, df):
        clustering=KMeans(n_clusters=5)
        y_pred=clustering.fit_predict(df)
        return y_pred
    