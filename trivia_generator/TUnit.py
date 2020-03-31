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
    :param article_id: the ID of the Wikipedia article.
    :type article_id: int
    :param url: the url of the Wikipedia article.
    :type url: str
    :param categories: a list of strings representing the titles of the categories the article belongs to.
    :type categories: List[str]
    :param access_timestamp: the Unix timestamp at which the article was accessed by the WebScraper.
    :type access_timestamp: int

    :param has_superlative: a boolean value representing whether the sentence has a superlative in it.
    :type has_superlative: int
    :param has_contrasting: a boolean value representing whether the sentence has a contrasting word in it.
    :type has_contrasting: int
    :param root_word: the root word of the sentence.
    :type root_word: str
    :param subj_word: the subject of the sentence.
    :type subj_word: str
    :param readability: the Gunning FOG index of sentence (see https://www.readabilityformulas.com/gunning-fog-readability-formula.php)
    :type readability: int

    :param t_unit_id: the auto-assigned id of the TUnit in the database
    :type t_unit_id: int
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
    article_id: int
    url: str

    access_timestamp: int

    has_superlative: int
    has_contrasting: int
    readability: int

    t_unit_id: int = None

    latitude: float = None
    longitude: float = None

    num_likes: int = 0
    num_mehs: int = 0
    num_dislikes: int = 0


    def to_tsv_line(self) -> str:
        return '\t'.join([str(attribute) for attribute in
            [
                self.sentence,
                self.article_id,
                self.url,
                self.access_timestamp,
                self.has_superlative,
                self.has_contrasting,
                self.readability,
                self.t_unit_id,
                self.latitude,
                self.longitude,
                self.num_likes,
                self.num_mehs,
                self.num_dislikes
            ]
        ])

    def __str__(self):
        return f"""TUnit:
  - Sentence: '{self.sentence[:137]}...'
  - Article ID: {self.article_id}
  - URL: {self.url}
  - Access Timestamp: {self.access_timestamp}
  - Coordinates:  ({self.latitude}, {self.longitude})
  - Has Superlative: {self.has_superlative}
  - Has Contrasting Phrases: {self.has_contrasting}
  - Readability (FOG): {self.readability}
  - Trivia Rank: {self.trivia_rank}
  - Question Rank: {self.question_rank}"""

def tunit_list_to_tsv(tunits: list, output_filename = 'tunits.tsv'):
    csv_output = '\n'.join([tunit.to_tsv_line() for tunit in tunits]) + '\n'
    with open(output_filename, 'a+') as f:
        f.write(csv_output)
