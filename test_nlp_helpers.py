from nlp_helpers import NLPConn
from nlp_helpers import ContradictatoryMatcher
from nlp_helpers import features

nlp = NLPConn.get_nlp_conn()

def test_get_has_superlatives():
    test_suite = [
        ("This is a sentence.", 0),
        ("This is the best sentence.", 1),
        ("I'm the smartest person to ever eat ice cream.", 1),
        ("I like pies.", 0),
        ("I like most pies.", 1),
        ("I like the most pies.", 1)
    ]
    for sentence_str, result in test_suite:
        sentence = nlp(sentence_str.lower())
        has_superlatives = features.get_has_superlatives(sentence)
        print(sentence_str)
        assert result == has_superlatives

def test_get_has_contradictatory():
    test_suite = [
        ("This is a sentence.", 0),
        ("Although this is a sentence, it is not a very good one.", 1),
        ("He is rich but he is also very poor.", 1),
        ("In spite of the global crisis, we must put on the best faces we can.", 1),
        ("It is not that he is gay, rather he is bisexual.", 1),
        ("He holds contrary viewpoints.", 0)
    ]

    for sentence_str, result in test_suite:
        sentence = list(nlp(sentence_str.lower()).sents)[0]
        has_contradictatory = features.get_has_contradictatory(sentence)
        print(sentence_str)
        assert result == has_contradictatory

def test_get_fog_score():
    test_suite = [
        ("This is a sentence.", 1.600),
        ("Although this is a sentence, it is not a very good one.", 4.800),
        ("In spite of the global crisis, we must put on the best faces we can.", 6.000),
        ("It is not that he is gay, rather he is bisexual.", 8.036),
        ("He holds contrary viewpoints.", 11.600),
        ("", 0)

    ]

    for sentence_str, result in test_suite:
        sentence = nlp(sentence_str.lower())
        fog_score = round(features.get_fog_score(sentence), 3)
        print(sentence_str)
        assert result == fog_score