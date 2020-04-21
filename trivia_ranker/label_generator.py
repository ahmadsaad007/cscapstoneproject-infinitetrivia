# Handle import junk
top_level_dir = os.path.abspath('../')
# include trivia generator modules
sys.path.append(top_level_dir)

from nlp_helpers import features
from trivia_ranker import feature_engineering
import pickle

def generate_labels(sentence_list):
    """
    This function gets the list of trivia sentences and generates their interistingness ranking
    using the pre-trained model
    """
    #get ner_ratios/counts
    ner_ratio = feature_engineering.get_ner_counts(sentence_list)
    #get Unigram features
    uni_features = feature_engineering.get_unigram_features(sentence_list)
    #get linguistic features
    has_super = []
    has_contra = []
    fog = []
    
    for sentence in sentence_list:
        has_super.append(features.get_has_superlatives(sentence))
        has_contra.append(features.get_has_superlatives(sentence))
        fog.append(features.get_fog_score(sentence))
    
    
    X_test =[]
    for index in range(len(sentence_list)):
        X_test.append([ner_ratio[index], uni_features[index], has_contra[index], has_super[index], fog[index]])
    
    loaded_model = pickle.load(open("svm.sav", 'rb'))
    generated_label = loaded_model.predict()
    y_test = loaded_model.predict(X_test)
    
    return y_test