import numpy as np 
import pandas as pd 
import tensorflow as tf 
from tensorflow import keras
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

class MLPNN:
    def __init__(self):
        print("Running Neural Network")
    def graph(self):
        print()
    def predictModel(self, path, dataArray):

        predictionLabels=["eyesOpen", "eyesCLosed", "Opposite Side", "Same Side", "Seizure"]
        model=keras.models.load_model(path)
        seizureAmount=0
        for rows in range(dataArray.shape[0]):
            
            newdf=dataArray.iloc[rows:rows+1]
            prediction_features = model.predict(newdf)
            print(prediction_features)
            if predictionLabels[np.argmax(prediction_features[0])] =="Seizure":
                seizureAmount+=1
        
        return seizureAmount

            
    def runModel(self, training_df, testing_df):
        #preprocessing for ml
        #training
        labels_train=training_df['Output']
        features_train=training_df.drop(columns=['Output'])
        features_train = features_train.values.astype('float32')
        labels_train = labels_train.values.astype('float32')
        #testing
        labels_test=testing_df['Output']
        features_test=testing_df.drop(columns=['Output'])
        features_test = features_test.values.astype('float32')
        labels_test = labels_test.values.astype('float32')
        #trainging, validation, and testing 
        """
        features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.2)
        features_train, features_validation, labels_train, labels_validation = train_test_split(features_train, labels_train, test_size=0.4)
        """
        features_train, features_validation, labels_train, labels_validation = train_test_split(features_train, labels_train, test_size=0.3)
        #setting up the neural network
        model = keras.Sequential([keras.layers.Dense(128, input_shape=(5,)),
                                keras.layers.Dense(128, activation=tf.nn.relu),
                                keras.layers.Dense(48, activation='linear'),
                                keras.layers.Dense(2,activation='softmax')])
        model.compile(optimizer='Adadelta',
             loss='sparse_categorical_crossentropy',
             metrics=['acc'])
        #running the actual Model
        
        history = model.fit(features_train, labels_train, epochs=100, validation_data=(features_validation, labels_validation))
        prediction_features = model.predict(features_test)
        performance = model.evaluate(features_test, labels_test)
        print(performance)
        history_dict = history.history
        #checking for overfitting
        acc = history_dict['acc']
        val_acc = history_dict['val_acc']
        loss = history_dict['loss']
        val_loss = history_dict['val_loss']
        epochs = range(1, len(acc) + 1)
        #plotting the data
        plt.plot(epochs, val_loss, 'b', label='Validation loss')
        plt.title('Training and validation loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()
        #model.save("my_model.h5")
        return history
    