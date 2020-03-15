"""
NLP Pre-processor
=================
"""

import spacy
from spacy.tokens import Span, Token
from spacy.matcher import PhraseMatcher

from web_scraper import Article
from web_scraper import get_page_by_random
from TUnit import TUnit


def _init_contradictatory_matcher():
    with open('contradictatory.txt', 'r') as f:
        contradictatory_words = f.read().splitlines()
        contradictatory_matcher = PhraseMatcher(nlp.vocab)
        patterns = [nlp.make_doc(text) for text in contradictatory_words]
        contradictatory_matcher.add("ContradictoryTokens", None, *patterns)
        return contradictatory_matcher

nlp = spacy.load("en_core_web_sm")
contradictatory_matcher = _init_contradictatory_matcher()

def _lemmatize(tok):
    return tok.lemma_.lower().strip() if tok.lemma_ != "-PRON-" else tok.lower_

def _count_syllables(word):
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

def _get_features(sentence: spacy.tokens.Span) -> tuple:
    has_superlatives = any([t.tag_ == 'JJS' for t in sentence])
    has_contradictatory = any(contradictatory_matcher(nlp(sentence.string)))

    sent_subjs = [t for t in sentence if t.dep_ == 'nsubj']
    sent_subj = _lemmatize(sent_subjs[0]) if sent_subjs else None

    num_complex_words = len([t for t in sentence if _count_syllables(t.text) > 2])

    fog = 0.4 * (len(sentence) + 100 * num_complex_words / len(sentence))
    fog = 0 if fog < 7 else 1 if fog < 15 else 2

    return (
        has_superlatives,
        has_contradictatory,
        _lemmatize(sentence.root),
        sent_subj,
        fog
    )

def create_TUnits(article: Article) -> list:
    """Creates a list of TUnits from a Wikipedia article object.

    :param article: A Wikipedia article object.
    :type article: Article

    :returns: a list of TUnits created from article.
    """

    paragraphs = ' '.join([para for para in article.content.splitlines() if para != ''])
    tunits = []
    doc = nlp(paragraphs)

    for sent in list(doc.sents):
        # print(sent)
        has_superlatives, has_contradictatory, sent_root, sent_subj, fog = _get_features(sent)
        tunits.append(
            TUnit(
                sent.string,
                1,
                article.url,
                article.categories,
                article.access_timestamp,
                has_superlatives,
                has_contradictatory,
                sent_root,
                sent_subj,
                fog,
                article.latitude,
                article.longitude,
                None,
                None
            )
        )
   

    return tunits

def _to_TUnit(article: Article) -> TUnit:
    pass

if __name__ == '__main__':
    article = get_page_by_random()
    tunits = create_TUnits(article)
    for tunit in tunits:
        print(tunit)