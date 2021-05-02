
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
class LinnearRegression():
    def __init__(self):
        print("Running kmeans Network")
    def runModel(self, df):
        reg=linear_model.LinearRegression()
        reg.fit(df.drop(columns=['Output']), df['Output'])
        print(reg.predict(df.drop(columns=['Output']).loc[1]))