"""
NLP Pre-processor
=================
"""
import os

import spacy
from spacy.tokens import Span, Token

from trivia_generator.web_scraper import Article
from trivia_generator.web_scraper.WebScraper import get_page_by_random
from trivia_generator.TUnit import TUnit

from nlp_helpers import features
from nlp_helpers import NLPConn
from nlp_helpers import ContradictatoryMatcher

nlp = NLPConn.get_nlp_conn()
contradictatory_matcher = ContradictatoryMatcher.get_contradicatory_matcher()

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
        has_superlatives = features.get_has_superlatives(sent)
        has_contradictatory = features.get_has_contradictatory(sent)
        fog = features.get_fog_score(sent)

        tunits.append(
            TUnit(
                sent.string,
                article.article_id,
                article.url,
                article.access_timestamp,
                has_superlatives,
                has_contradictatory,
                fog,
                None,
                article.latitude,
                article.longitude,
                0,
                0,
                0
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
