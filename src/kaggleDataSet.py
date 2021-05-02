import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt


#getting the data
seizure_df=pd.read_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/Epileptic Seizure Recognition.csv")
seizure_df=seizure_df.sort_values('Unnamed')
'''
def graph():
    x1=seizure_df.head(500)
    x1.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x1.csv",index=False )

    x2=seizure_df.iloc[501:1000]
    x2.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x2.csv", index=False)

    x3=seizure_df.iloc[1001:1500]
    x3.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x3.csv", index=False)

    x4=seizure_df.iloc[1501:2000]
    x4.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x4.csv", index=False)

    x5=seizure_df.iloc[2001:2500]
    x5.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x5.csv", index=False)

    x6=seizure_df.iloc[2501:3000]
    x6.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x6.csv", index=False)

    x7=seizure_df.iloc[3001:3500]
    x7.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x7.csv", index=False)

    x8=seizure_df.iloc[3501:4000]
    x8.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x8.csv", index=False)

    x9=seizure_df.iloc[501:1000]
    x9.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x9.csv", index=False)

    x10=seizure_df.iloc[4501:5000]
    x10.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x10.csv", index=False)

    x11=seizure_df.iloc[5001:5500]
    x11.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x11.csv", index=False)

    x12=seizure_df.iloc[5501:6000]
    x12.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x12.csv", index=False)

    x13=seizure_df.iloc[6001:6500]
    x13.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x13.csv", index=False)

    x14=seizure_df.iloc[6501:7000]
    x14.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x14.csv", index=False)

    x15=seizure_df.iloc[7001:7500]
    x15.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x15.csv", index=False)

    x16=seizure_df.iloc[7501:8000]
    x16.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x16.csv", index=False)

    x17=seizure_df.iloc[8001:8500]
    x17.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x17.csv", index=False)

    x18=seizure_df.iloc[8501:9000]
    x18.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x18.csv", index=False)

    x19=seizure_df.iloc[9001:9500]
    x19.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x19.csv", index=False)

    x20=seizure_df.iloc[9501:10000]
    x20.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x20.csv", index=False)

    x21=seizure_df.iloc[10001:10500]
    x21.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x21.csv", index=False)

    x22=seizure_df.iloc[10501:11000]
    x22.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x22.csv", index=False)

    x23=seizure_df.iloc[11001:11500]
    x23.to_csv("C:/Users/Nathan Joseph/Desktop/CPEG498/SortedData/x23.csv", index=False)
'''
#getting the input variables and output varaibles
input_variable_df=seizure_df.drop('y', axis=1)
input_variable_df=seizure_df.drop('Unnamed', axis=1)
output_variable_df=seizure_df['y']

#training modules
linear_regression = LinearRegression()

#splitting data into training set and testing set
x_train, x_test, y_train, y_test=train_test_split(input_variable_df, output_variable_df, test_size=0.3)


#running a linnear regression model on data
linear_regression.fit(x_train, y_train)


#testing module
y_pred=linear_regression.predict(x_test)
#score =linear_regression.score(x_test.values, y_test.values)

#evaluating our data:
#
#for rowNum in range(len(y_test)):
 #   print ("Predicted: "+ str(y_pred[rowNum]) + ", Actual: " + str(y_test.iloc[rowNum]))
    #if(abs(y_pred[rowNum]-y_test.iloc[rowNum])>0.0000000000001):
     #   print ("Predicted: "+ str(y_pred[rowNum]) + ", Actual: " + str(y_test.iloc[rowNum]))