from .Article import Article


def get_page_by_category(category: str) -> Article:
    """Gets the contents and metadata of a Wikipedia article with a given category.

    :param category : the category with which to search.
    :return : the Article object representing the Wikipedia article.

    """
    pass


def get_page_by_random() -> Article:
    """Gets the contents and metadata of a random Wikipedia article.
    
    :return : the Article object representing the Wikipedia article.
    """
    pass


def get_page_by_location(longitude: float, latitude: float) -> Article:
    """Gets the contents and metadata of a Wikipedia article close to the given coordinates.
    
    :return : the Article object representing the Wikipedia article.
    """
    pass
