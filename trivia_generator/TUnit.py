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

    :param t_unit_id: the auto-assigned id of the TUnit in the database
    :type t_unit_id: int
    :param longitude: the longitude of the physical location of the article, if relevant.
    :type longitude: float
    :param latitude: the latitude of the physical location of the article, if relevant.
    :type latitude: float
    """

    sentence: str
    article_id: int
    url: str

    access_timestamp: int

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
                self.t_unit_id,
                self.latitude,
                self.longitude,
                self.num_likes,
                self.num_mehs,
                self.num_dislikes
            ]
        ])

    def __str__(self):
        return f"""TUnit (ID: ${self.t_unit_id}):
  - Sentence: '{self.sentence[:137]}...'
  - Article ID: {self.article_id}
  - URL: {self.url}
  - Access Timestamp: {self.access_timestamp}
  - Coordinates:  ({self.latitude}, {self.longitude})
  - Number of Likes/Mehs/Dislikes: {self.num_likes}/{self.mehs}/{self.num_dislikes}"""

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

def tunit_list_to_tsv(tunits: list, output_filename='tunits.tsv'):
    csv_output = '\n'.join([tunit.to_tsv_line() for tunit in tunits]) + '\n'
    with open(output_filename, 'a+') as f:
        f.write(csv_output)
