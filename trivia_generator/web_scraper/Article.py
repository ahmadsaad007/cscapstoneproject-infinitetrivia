from dataclasses import dataclass


@dataclass
class Article:
    """Representation of a Wikipedia article and its metadata.

    :param content : the text of the Wikipedia article, cleaned of HTML tags.
    :param url : the url of the Wikipedia article
    :param categories : a list of strings representing the titles of the categories the article belongs to.
    :param access_timestamp : the Unix timestamp at which the article was accessed by the WebScraper.
    
    :param longitude : the longitude of the physical location of the article, if relevant.
    :param latitude : the latitude of the physical location of the article, if relevant.
    """
    content: str
    url: str
    categories: list
    access_timestamp: int

    longitude: float = None
    latitude: float = None
