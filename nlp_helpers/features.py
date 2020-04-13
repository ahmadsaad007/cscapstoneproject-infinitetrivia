import spacy

from nlp_helpers import NLPConn
from nlp_helpers import ContradictatoryMatcher

def get_has_superlatives(sentence: spacy.tokens.Span) -> int:
    return int(any([t.tag_ == 'JJS' for t in sentence]))

def get_has_contradictatory(sentence) -> int:
    if type(sentence) == spacy.tokens.Span:
        nlp = NLPConn.get_nlp_conn()
        sentence = nlp(sentence.string)
    
    contradictatory_matcher = ContradictatoryMatcher.get_contradicatory_matcher()
    return int(any(contradictatory_matcher(sentence)))

def get_fog_score(sentence) -> float:
    num_complex_words = len([t for t in sentence if count_syllables(t.text) > 2])
    num_words = len([t for t in sentence if not t.is_punct])
    if num_words == 0:
        return 0
    
    fog = 0.4 * (num_words + 100 * num_complex_words / num_words)
    # fog = 0 if fog < 7 else 1 if fog < 15 else 2
    return fog

def lemmatize(tok) -> str:
    return tok.lemma_.lower().strip() if tok.lemma_ != "-PRON-" else tok.lower_

def count_syllables(word) -> int:
    syllable_count = 0
    vowels = 'aeiouy'
    if word[0] in vowels:
        syllable_count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllable_count += 1
    if word.endswith('e'):
        syllable_count -= 1
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        syllable_count += 1
    if syllable_count == 0:
        syllable_count += 1
    return syllable_count

def is_complete_sentence(sentence) -> bool:
    # If sentence begins with a capital letter and ends with punctuation.
    if sentence[-1].is_punct:
        num_nouns = len([tok for tok in sentence if tok.pos_ in ["NOUN", "PROPN", "PRON"]])
        num_verbs = len([tok for tok in sentence if tok.pos_ == "VERB"])

        if type(sentence) == spacy.tokens.Span:
            root_word = sentence.root
        else:
            root_word = list(sentence.sents)[0].root

        # Complete sentence has subject (noun), verb, and object (noun).
        # The verb should be the root of the sentence.
        return num_nouns >= 2 and num_verbs >= 1 and root_word.pos_ == "VERB"
    else:
        return False

def sentence_has_context(sentence) -> bool:
    if type(sentence) == spacy.tokens.Span:
        nlp = NLPConn.get_nlp_conn()
        sentence = nlp(sentence.string)
    
    sent_subjs = [t for t in sentence if t.dep_ == 'nsubj']
    return any([subj for subj in sent_subjs if subj.pos_ == "PROPN"])

def resolve_coreferences(content: str) -> str:
    nlp = NLPConn.get_nlp_conn()
    doc = nlp(content)
    resolved_coref = doc._.coref_resolved
    print(resolved_coref)
    return resolved_coref