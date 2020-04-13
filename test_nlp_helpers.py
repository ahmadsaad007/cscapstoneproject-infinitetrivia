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
    for sentence_str, expected in test_suite:
        sentence = nlp(sentence_str.lower())
        result = features.get_has_superlatives(sentence)
        print(sentence_str)
        assert expected == result

def test_get_has_contradictatory():
    test_suite = [
        ("This is a sentence.", 0),
        ("Although this is a sentence, it is not a very good one.", 1),
        ("He is rich but he is also very poor.", 1),
        ("In spite of the global crisis, we must put on the best faces we can.", 1),
        ("It is not that he is gay, rather he is bisexual.", 1),
        ("He holds contrary viewpoints.", 0)
    ]

    for sentence_str, expected in test_suite:
        sentence = list(nlp(sentence_str.lower()).sents)[0]
        result = features.get_has_contradictatory(sentence)
        print(sentence_str)
        assert expected == result

def test_get_fog_score():
    test_suite = [
        ("This is a sentence.", 1.600),
        ("Although this is a sentence, it is not a very good one.", 4.800),
        ("In spite of the global crisis, we must put on the best faces we can.", 6.000),
        ("It is not that he is gay, rather he is bisexual.", 8.036),
        ("He holds contrary viewpoints.", 11.600),
        ("", 0)

    ]

    for sentence_str, expected in test_suite:
        sentence = nlp(sentence_str.lower())
        result = round(features.get_fog_score(sentence), 3)
        print(sentence_str)
        assert expected == result

def test_is_complete_sentence():
    test_suite = [
        ("I eat an apple.", True),
        ("Eat an apple.", False),
        ("I eat.", False),
        ("Eat an apple.", False),
        ("During his childhood, Downey had minor roles in his father's films.", True),
        ("In April 2001, while he was on parole", False),
        ("In 2006, Downey returned to television when he did voice acting on Family Guy in the episode \"The Fat Guy Strangler\".", True),
        ("Main articles: Robert Downey Jr. filmography and List of awards and nominations received by Robert Downey Jr.", False),
        ("John may also refer to: ", False),
        ("Third Epistle of John, often shortened to 3 John", False)
    ]

    for sentence_str, expected in test_suite:
        sentence = nlp(sentence_str.lower())
        print(sentence_str)
        result = features.is_complete_sentence(sentence)
        assert expected == result

def test_sentence_has_context():
    test_suite = [
        ("I eat an apple.", False),
        ("Eat an apple.", False),
        ("I eat.", False),
        ("Eat an apple.", False),
        ("During his childhood, Downey had minor roles in his father's films.", True),
        ("In April 2001, while he was on parole", False),
        ("In 2006, Downey returned to television when he did voice acting on Family Guy in the episode \"The Fat Guy Strangler\".", True),
        ("Main articles: Robert Downey Jr. filmography and List of awards and nominations received by Robert Downey Jr.", False),
        ("John may also refer to: ", True)
    ]

    for sentence_str, expected in test_suite:
        sentence = nlp(sentence_str.lower())
        print(sentence_str)
        result = features.sentence_has_context(sentence)
        assert expected == result
