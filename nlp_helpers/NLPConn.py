import spacy
import neuralcoref

nlp = None

def get_nlp_conn():
    global nlp
    if nlp is None:
        nlp = spacy.load('en_core_web_lg')
        neuralcoref.add_to_pipe(nlp)
    return nlp