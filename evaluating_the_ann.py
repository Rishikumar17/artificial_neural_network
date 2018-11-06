# -*- coding: utf-8 -*-
"""
This project has been made with the help of Google Colaboratory.
Also the dataset used is Churns Modelling.csv and opensource dataset provided by the SuperDataScience
"""
# Load the Drive helper and mount
#The ChurnModelling.csv file was saved in my Google Drive and hence the following commands
#Uncomment it if you want 

#from google.colab import drive

# This will prompt for authorization.

#drive.mount('/content/drive')

#lists the content of your google drive
# !ls "/content/drive/My Drive"

#Importing Libraries that will be used throughout this code snippet

#Pandas for preprocessing data
import pandas as pd
#Used for initialising a neural network
from keras.models import Sequential
#Dropout is used for preventing over-fitting
from keras.layers import Dropout
#Dense layer is used for creating an fully-connected layer
from keras.layers import Dense
#StandardScalar is used for scaling the values in a particular range
from sklearn.preprocessing import StandardScaler
#train_test_split is used for splitting the dataset into training and testing set
from sklearn.model_selection import train_test_split
#Implementing K-fold which is sklearn package but needs to be implemented with Keras
from keras.wrappers.scikit_learn import KerasClassifier
#Retrieving cross validation score
from sklearn.model_selection import cross_val_score
#Used mainly for implementing a Grid Search which is used for hypertuning the parameters
from sklearn.model_selection import GridSearchCV

#Reading the dataset of .csv format
dataset = pd.read_csv("/content/drive/My Drive/Churn_Modelling.csv")
#Prints the first 5 rows from the dataset
#dataset.head()

#Getting dependant values that needs to be predicted
Y = dataset.iloc[:,13]

#Getting independant values
X = dataset.iloc[:,0:13]
#Gets the shape of the independant data
#X.shape

#Removing all the non-required columns
X.drop(["RowNumber","CustomerId","Surname"],axis = 1,inplace = True)

#Getting the dummy value of Geography (categorical values)
#Dropping the first column to avoid the dummy value trap
geography = pd.get_dummies(X["Geography"], drop_first=True)

#Getting the dummy value of Gender (categorical values)
#Dropping the first column to avoid the dummy value trap
sex = pd.get_dummies(X["Gender"], drop_first=True)

#Merging the dummy values of geography , gender with the original dataset and dropping the original columns
X = pd.concat([X,geography,sex], axis=1)
X.drop(["Geography","Gender"], axis=1,inplace=True)

#Splitting the dataset into 80%-20% ratio with a random seed of 20  
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = 0.2, random_state = 20)

#Used for scaling the independant variable values
sc_x = StandardScaler()
X_train = sc_x.fit_transform(X_train)
X_test = sc_x.transform(X_test)

"""Part 1 and Part 4
Part 1 includes building a noraml artificial neural network without a dropout layer and Part 4 includes adding a Dropout layer for
Overfitting
Building a neural network"""

#Initialising the neural network 
classifier = Sequential()
#Adding the input and first hidden layer
classifier.add(Dense(units = 6, activation='relu', kernel_initializer= 'uniform', input_dim = 11))
#Adding the second hidden layer
classifier.add(Dense(units = 6, activation='relu', kernel_initializer='uniform'))
#Adding the output layer
classifier.add(Dense(units = 1, activation='sigmoid', kernel_initializer='uniform'))
#Compiling the Artificial neural network
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
#Fitting the ANN
classifier.fit(X_train, y_train, epochs=100, batch_size=10)

#Predicting with this models
#This is the possibility of an individual leaving the bank (in probability outcomes)
y_pred = classifier.predict(X_test)

#This is the possibility of an individual leaving the bank 
y_pred = (y_pred > 0.5)

#Part 2
#Evaluating a neural network
#Evaluating the ANN
def build_classifier():
  classifier = Sequential()
  classifier.add(Dense(units = 6, activation='relu', kernel_initializer= 'uniform', input_dim = 11))
  classifier.add(Dense(units = 6, activation='relu', kernel_initializer='uniform'))
  classifier.add(Dense(units = 1, activation='sigmoid', kernel_initializer='uniform'))
  classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
  return classifier

#Fitting the model with 10 different K-folds
classifier = KerasClassifier(build_fn = build_classifier, batch_size = 10, epochs = 100)
#Applying K-fold cross validation where K = 10
accuracies = cross_val_score(estimator = classifier, X=X_train, y=y_train, cv=10, n_jobs = -1)

#Getting the mean and stddev of all the accuracies
mean = accuracies.mean()
variance = accuracies.std()

