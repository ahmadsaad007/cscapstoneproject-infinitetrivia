from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_scoreimport csv
import numpy as np

def trivia_classifier():
    """
    The functions reads in the trivia file, extracts the feature columns, performs K-folds Cross validation, 
    Trains an SVM classifier with a linear kernel and then tests it
    """
    # Read the training data file
    szDatasetPath = 'training_data.csv'
    listClasses = []
    listAttrs = []
    bFirstRow = True
    with open(szDatasetPath, encoding="utf8") as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        for row in csvReader:
            if bFirstRow:
                bFirstRow = False
                continue
            listClasses.append(row[-1])
            listAttrs.append(list(map(float, row[1:4])))
    """Added a column of 1's to the data"""
    #for i in range(len(listAttrs)):
    #    listAttrs[i].append(1.0)
    dataX = np.array(listAttrs)
    dataY = np.array(listClasses)
    
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
    
    predictY = clf.predict(X_test)
    print("Accuracy ",accuracy_score(y_test, predictY))
    return None