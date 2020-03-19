"""
Article
=======
"""

from dataclasses import dataclass


@dataclass
class Article:
    """Representation of a Wikipedia article and its metadata.

    :param content: the text of the Wikipedia article, cleaned of HTML tags.
    :type content: str
    :param url: the url of the Wikipedia article
    :type url: str
    :param categories: a list of strings representing the titles of the categories the article belongs to.
    :type categories: List[str]
    :param access_timestamp: the Unix timestamp at which the article was accessed by the WebScraper.
    :type access_timestamp: int
    :param article_id: the id_of the Wikipedia article from which the TUnit originated.
    :type article_id: int
    :param latitude: the latitude of the physical location of the article, if relevant (default: None).
    :type latitude: float
    :param longitude: the longitude of the physical location of the article, if relevant (default: None).
    :type longitude: float
    """
    content: str
    url: str
    article_id: int
    categories: list
    access_timestamp: int
    
    latitude: float = None
    longitude: float = None

    def __str__(self):
        categories_str = '\n      - '.join(self.categories)
        return f"""Article:
  - Content: '{self.content[:137]}...'
  - URL: {self.url}
  - Article ID: {self.article_id}
  - Categories:
      - {categories_str}
  - Access Timestamp: {self.access_timestamp}
  - Coordinates: ({self.latitude}, {self.longitude})"""