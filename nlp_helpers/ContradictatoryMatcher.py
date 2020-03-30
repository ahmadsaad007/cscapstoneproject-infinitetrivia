from spacy.matcher import PhraseMatcher

import os

from nlp_helpers import NLPConn

TOP_LEVEL_DIR = os.path.abspath('../')
contradictory_path = TOP_LEVEL_DIR + '/contradictatory.txt'

matcher = None

def get_contradicatory_matcher():
    global matcher
    if matcher is None:
        nlp = NLPConn.get_nlp_conn()
        with open(contradictory_path, 'r') as f:
            contradictatory_words = f.read().splitlines()
            matcher = PhraseMatcher(nlp.vocab)
            patterns = [nlp.make_doc(text) for text in contradictatory_words]
            matcher.add("ContradictoryTokens", None, *patterns)
    return matcher
