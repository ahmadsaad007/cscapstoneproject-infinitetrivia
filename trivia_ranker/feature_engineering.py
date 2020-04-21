# Handle import junk
top_level_dir = os.path.abspath('../')
# include trivia generator modules
sys.path.append(top_level_dir)

import itertools
import spacy
import csv
import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nlp_helpers import features
from nlp_helpers import NLPConn
from nlp_helpers import ContradictatoryMatcher
from trivia_generator.web_scraper import WebScraper
from trivia_generator import NLPPreProcessor
from trivia_generator import TUnit

nlp = NLPConn.get_nlp_conn()

def get_ner_counts(sentences):
    ner_ratio = []
    for sentence in sentences:
        doc = nlp(sentence)
        ner_counts = 0
        for ent in doc.ents:
            if(ent.label_ == "PERSON" or ent.label_ == "MONEY" or ent.label_ == "EVENT" or 
                ent.label_ == "ORDINAL" or ent.label_ == "LANGUAGE" or ent.label_ == "WORK_OF_ART" 
                or ent.label_ == "GPE" or ent.label_ == "LOC"):
                ner_counts = ner_counts + 1
        ner_ratio.append(ner_counts/len(doc))
    return ner_ratio

def get_unigram_features(sentences):
    
    vectorizer = TfidfVectorizer(smooth_idf=True, use_idf=True, stop_words = "english") #max_features = 1000
    X = vectorizer.fit_transform(sentences)
    
    df = pd.DataFrame(X.toarray(),columns = vectorizer.get_feature_names())
    
    df["idf_Avg"] = df.sum(axis=1)/len(df.columns)
    idf_Sum = df['idf_Avg'].values.tolist()
    return idf_Sum

def read_csv(fileName):
    
    features_list = []
    with open(fileName, 'r',newline = '', encoding='utf-8', errors='ignore') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            features = [row[0], row[7], row[8], row[9]]
            features_list.append(features)
    return features_list

def generate_training_data():
    
    article = WebScraper.get_page_by_random()
    tunits = NLPPreProcessor.get_TUnits(article)
    TUnit.tunit_list_to_tsv(tunits)
    
    corpus_data = read_csv("tunits.tsv")
    sentence_list=[]
    for line in corpus_data:
        sentence_list.append(line[0].lower())
    #get ner_ratios/counts
    ner_ratio = get_ner_counts(sentence_list)

    #get Unigram features
    uni_features = get_unigram_features(sentence_list)
    
    #get linguistic features
    has_super = []
    has_contra = []
    fog = []
    for sentence in sentence_list:
        has_super.append(features.get_has_superlatives(sentence))
        has_contra.append(features.get_has_superlatives(sentence))
        fog.append(features.get_fog_score(sentence))
    
    #get likeness_ratio
    like_ratios = []
    for line in corpus_data:
        likes = int(line[1])
        mehs = int(line[2])
        dislikes = int(line[3])
        total_votes = likes + mehs + dislikes
        if(total_votes == 0):
            value = 0
        else:
            value = (likes + 0.5*mehs)/total_votes
        if(value < 0.45):
            label = 0
        elif(value > 0.75):
            label = 2
        else:
            label = 1
        like_ratios.append(label)
    
    #write data to csv
    with open('training_data.csv','w', newline='') as file:
        wr = csv.writer(file, dialect='excel', delimiter=',')
        for index in range(len(sentence_list)):
            wr.writerow([sentence_list[index], ner_ratio[index], uni_features[index], has_contra[index], has_super[index], fog[index], like_ratios[index]])


generate_training_data()