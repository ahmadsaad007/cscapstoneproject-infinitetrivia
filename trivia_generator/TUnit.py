"""
TUnit
=====
"""

from dataclasses import dataclass


@dataclass
class TUnit:
    """Representation of a trivia unit and its associated metadata.

    :param sentence: the original sentence from Wikipedia.
    :param url: the url of the Wikipedia article.
    :param categories: a list of strings representing the titles of the categories the article belongs to.
    :param access_timestamp: the Unix timestamp at which the article was accessed by the WebScraper.

    :param has_superlative: a boolean value representing whether the sentence has a superlative in it.
    :param has_contrasting: a boolean value representing whether the sentence has a contrasting word in it.
    :param root_word: the root word of the sentence.
    :param subj_word: the subject of the sentence.
    :param readability: the Gunning FOG index of sentence (see https://www.readabilityformulas.com/gunning-fog-readability-formula.php)

    :param longitude: the longitude of the physical location of the article, if relevant.
    :param latitude: the latitude of the physical location of the article, if relevant.
    :param trivia_rank: the "trivianess" of the sentence (default: None).
    :param question_rank: how well the question is phrased (default: None).
    """

    sentence: str
    url: str
    categories: list
    access_timestamp: int

    has_superlative: bool
    has_contrasting: bool
    root_word: str
    subj_word: str
    readability: int

    latitude: float = None
    longitude: float = None

    trivia_rank: int = None
    question_rank: int = None
