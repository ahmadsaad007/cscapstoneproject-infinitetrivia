import itertools

import numpy as np
from scipy import stats
import pylab as pl
from sklearn import svm, linear_model
import sklearn.model_selection
import spacy

from nlp_helpers import NLPConn

nlp = NLPConn.get_nlp_conn()

#Algorithm for Rank SVM for ranking the trivia
def rankSVM(trainX, trainY):
    """
    This is a ranking function which ranks the given trivia text based on the feature values
    """
    clf = svm.SVC(kernel='linear') # Linear Kernel
    #Train the model using the training sets
    clf.fit(trainX, trainY)
    #Predict the response for test dataset
    y_pred = clf.predict(X_test) 

def getTextFeatures(sentence):
    doc = nlp(sentence)
    #print(type(doc))
    likenessRatio= 1 #number of likes/total ratings 1 is just a temporary value.
    NERcounts = 0
    for ent in doc.ents:
        if(ent.label_ == "PERSON" or ent.label_ == "MONEY" or ent.label_ == "EVENT" or
           ent.label_ == "ORDINAL" or ent.label_ == "LANGUAGE" or ent.label_ == "WORK_OF_ART" 
           or ent.label_ == "GPE" or ent.label_ == "LOC"):
            NERcounts = NERcounts + 1
    
    NERValue = NERcounts/len(doc)
    print("Sentence: " + sentence)
    print("NERCount: "+ str(NERcounts))
    print("NERValue: "+ str(NERValue))
    linguisticFeatures(doc)
    print()
    return    

def linguisticFeatures(doc):
    """
    This method will find the following:
        a) Presence of superlatives : binary feature of 0 or 1
        b) Presence of Root word : binary feature of 0 or 1
        c) Presence of contradictory words : binary feature of 0 or 1. Still need to implement this.
        d) Readabilty score: maybe FOG : float value
    """
    has_root = 0
    has_superlatives = 0
    has_contradictory = 0
    FOG = 0.0
    
    contradictory_words = ["but", "although", "unlike", "nevertheless", "even though",
                           "still", "yet", "despite", "inspite of", "besides", "while", "unless",
                           "when", "rather than", "however", "nonetheless", "conversely", "instead", 
                           "otherwise", "rather"]
    """Have to use phrase matcher to look for contradictory words/phrases instead of token matcher"""
    complex_count = 0
    
    for token in doc:
        if(token.dep_== "ROOT"):
            has_root = 1
        #count of complex words. Complex words are words more than 9 letters long
        if (len(token) > 9):
            complex_count = complex_count + 1
        #Check if it contains superlative
        if(token.tag_ == "JJS" or token.tag_ == "RBS"):
            has_superlatives = 1
            
    FOG = (len(doc) + 100*(complex_count/len(doc)))*0.4
    print("Root Sprltv. Contrd. FOG")
    print(has_root, has_superlatives, has_contradictory, FOG)
    #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.is_alpha, token.is_stop)
    return

def unigramFeatures():
    """
    Yet to decide how to implement this. Theory:
    UnigramFeatures will detect the presence of certain words in a sentence. Two approaches:
        1) We define what the words are by hard coding them
        2) Create a bag of words representation of the sentences marked as interesting trivia. Do the same for current
        sentence and compute a similarity score (or just see how many words they have in common, excluding stop words 
        obviously). Problems: The vector will be sparse so finding the threshold value is a challenge. Also, we need
        to have a predefined set of sentences marked as interesting to perform this. 
        One possible solution is to implement this feature as a binary value which returns true if A WORD is detected
        (not the best approach in my opinion)
    """

def main():
    #read file and find interesting features:
    corpus = ["Elvis Presley was a prominent singer of the 20th century.",
              "Usain Bolt, the Jamaican runner is an 11-time world champion and holds the record in the 100 and 200 meter race.",
              "The first Wimbledon Championship was held in 1877.",
              "Christian Bale reportedly studied Tom Cruise’s mannerisms to prepare for his role as a serial killer Patrick Bateman in American Psycho.",
              "Gene Autry is the only person to be awarded stars in all five categories on the Hollywood Walk of Fame.",
              "The hashtag symbol is technically called an octothorpe.",
              "It’s been said that nearly 3% of the ice in Antarctic glaciers is penguin urine.",
              "Ahmad Saad is a student at Temple University.",
              "Apple is looking at buying U.K. startup for $1 billion.",
              "The Nile is the longest river in the world.", 
              "Defeated only once in roughly 300 matches, President Abraham Lincoln was inducted into the National Wrestling Hall Of Fame in 1992.",
              "A study published in the journal Anthrozoo reported that cows produce 5% more milk when they are given names.",
              "El Colacho is a Spanish festival where people dress up like the devil and jump over babies.", 
              "The band Queen's original name was Smile."]
    for sentence in corpus:
        getTextFeatures(sentence)
main()