import spacy

nlp = None

def get_nlp_conn():
    global nlp
    if nlp is None:
        nlp = spacy.load('en_core_web_lg')
    return nlp