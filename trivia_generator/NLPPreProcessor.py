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
        tunits.append(
            TUnit(
                sent.string,
                article.article_id,
                article.url,
                article.access_timestamp,
                None,
                article.latitude,
                article.longitude,
                0,
                0,
                0
            )
        )

    return tunits


if __name__ == '__main__':
    article = get_page_by_random()
    tunits = create_TUnits(article)
    for tunit in tunits:
        print(tunit)
