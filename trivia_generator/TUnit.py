"""
TUnit
=====
"""

from dataclasses import dataclass


@dataclass
class TUnit:
    """Representation of a trivia unit and its associated metadata.

    :param sentence: the original sentence from Wikipedia.
    :type sentence: str
    :param url: the url of the Wikipedia article.
    :type url: str
    :param categories: a list of strings representing the titles of the categories the article belongs to.
    :type categories: List[str]
    :param access_timestamp: the Unix timestamp at which the article was accessed by the WebScraper.
    :type access_timestamp: int

    :param has_superlative: a boolean value representing whether the sentence has a superlative in it.
    :type has_superlative: bool
    :param has_contrasting: a boolean value representing whether the sentence has a contrasting word in it.
    :type has_contrasting: bool
    :param root_word: the root word of the sentence.
    :type root_word: str
    :param subj_word: the subject of the sentence.
    :type subj_word: str
    :param readability: the Gunning FOG index of sentence (see https://www.readabilityformulas.com/gunning-fog-readability-formula.php)
    :type readability: int

    :param longitude: the longitude of the physical location of the article, if relevant.
    :type longitude: float
    :param latitude: the latitude of the physical location of the article, if relevant.
    :type latitude: float
    :param trivia_rank: the "trivianess" of the sentence (default: None).
    :type trivia_rank: int
    :param question_rank: how well the question is phrased (default: None).
    :type question_rank: int
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
