import numpy as np 
import pandas as pd 
import tensorflow as tf 
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow import keras
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from tensorflow.keras import datasets, layers, models
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.models import Sequential
import matplotlib.pyplot as plt
from keras.layers import Dense, Dropout, Conv2D, MaxPool2D, Flatten
from keras.utils import np_utils
class CNN:
    def __init__(self):
        print("Running CNN network")
    def graph(self, df, columnName, rowNum):
       subband=df[columnName][rowNum]
       plt.plot(subband)
       plt.show()
    #makes prediction
    def predictModel(self, path, dataArray):

        predictionLabels=["Seizure", " non Seizure"]
        model=keras.models.load_model(path)
        prediction_features = model.predict(dataArray)
        #print(prediction_features)
        if(prediction_features[0][1]==0):
            print ("Seizure")
        else:
            print ("Non seizure")
        #print( predictionLabels[np.argmax(prediction_features)])
         
    #runs model
    def runModel(self, training_array_input,testing_array_input,training_array_output,testing_array_output):
        #input data
        X_train=training_array_input
        X_test=testing_array_input
        X_train = X_train.astype('float32')
        X_test = X_test.astype('float32')
       
        #output data 
        y_train=training_array_output
        y_test=testing_array_output
       

        # building the input vector
        X_train = X_train.reshape(X_train.shape[0], 3, 342, 1)
        X_test = X_test.reshape(X_test.shape[0], 3, 342, 1)
        X_train = X_train.astype('float32')
        X_test = X_test.astype('float32')

        # one-hot encoding using keras' numpy-related utilities
        n_classes = 2
        Y_train = np_utils.to_categorical(y_train, n_classes)
        Y_test = np_utils.to_categorical(y_test, n_classes)
        # building a linear stack of layers with the sequential model
        model = Sequential()
        # convolutional layer
        model.add(Conv2D(25, kernel_size=(3,3), strides=(1,1), padding='valid', activation='relu', input_shape=(3,342,1)))
        model.add(MaxPool2D(pool_size=(1,1)))
        # flatten output of conv
        model.add(Flatten())
        # hidden layer
        
        model.add(Dense(100, activation='relu'))
        
        # output layer
        model.add(Dense(2, activation='softmax'))

        # compiling the sequential model
        model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

        # training the model for 10 epochs
        model.fit(X_train, Y_train, epochs=50, validation_data=(X_test, Y_test))
        model.save("my_model.h5")
        return model