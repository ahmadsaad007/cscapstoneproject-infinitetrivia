from spacy.matcher import PhraseMatcher

from nlp_helpers import NLPConn

contradictatory_phrases = [
    'although',
    'in contrast',
    'different from',
    'of course',
    'on the other hand',
    'on the contrary',
    'at the same time',
    'in spite of',
    'even so',
    'though',
    'be that as it may',
    'then again',
    'above all',
    'in reality',
    'after all',
    'but',
    'still',
    'unlike',
    'or',
    'yet',
    'while',
    'albeit',
    'besides',
    'as much as',
    'even though',
    'although',
    'instead',
    'whereas',
    'despite',
    'conversely',
    'otherwise',
    'however',
    'rather',
    'nevertheless',
    'nonetheless',
    'regardless',
    'notwithstanding'
]

matcher = None

def get_contradicatory_matcher():
    global matcher
    if matcher is None:
        nlp = NLPConn.get_nlp_conn()
        matcher = PhraseMatcher(nlp.vocab)
        patterns = [nlp.make_doc(phrase) for phrase in contradictatory_phrases]
        matcher.add("ContradictoryTokens", None, *patterns)
    return matcher
