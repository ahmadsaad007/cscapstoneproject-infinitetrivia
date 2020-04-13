from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score 
import csv
import numpy as np
import pickle
import time

def trivia_classifier():
    
    # Read the training data file
    szDatasetPath = 'training_data.csv'
    listClasses = []
    listAttrs = []
    
    with open(szDatasetPath, encoding="utf8", errors='ignore', newline='') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        #print(csvReader)
        for row in csvReader:
            listClasses.append(row[-1])
            listAttrs.append(list(map(float, row[1:5])))
    
    dataX = np.array(listAttrs)
    dataY = np.array(listClasses)
    print(len(listAttrs[0]))
    
    #train test split
    X_train, X_test, y_train, y_test = train_test_split(dataX, dataY, test_size=0.33, random_state=42)
    
    #perform k-folds on it
    k = 5
    foldsX = (np.array_split(X_train, k))
    foldsY = (np.array_split(y_train, k))
    clf = svm.SVC(kernel='linear', C = 1, gamma = 'auto')
    #Run a loop to get the folds. Fold[i] is the test data and remaining folds are the training data
    for i in range(k):
        print("FOLD #", i+1)
        
        trainX = foldsX.copy() 
        trainY = foldsY.copy()
        testX = foldsX[i]
        testY = foldsY[i]
        
        #Deleting the test data from the aggregate to perform k-fold cross validation
        del trainX[i]
        del trainY[i]
        
        trainX = np.concatenate(trainX,axis=0)
        trainY = np.concatenate(trainY,axis=0)
        clf.fit(trainX, trainY)
        print(clf.score(testX, testY))
    #Save the model to a file
    pickle.dump(clf, open("svm_model.sav", 'wb'))
    
    predictY = clf.predict(X_test)
    print("Accuracy ",accuracy_score(y_test, predictY))
    return None

trivia_classifier()