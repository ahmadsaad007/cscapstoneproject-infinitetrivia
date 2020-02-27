"""
WebScraper
==========

Gets contents and metadata from Wikipedia articles.
"""
import json
import random
import time

import requests
import bs4

from .Article import Article

ARTICLE_BY_ID_URL = 'http://enwp.org?curid='
RANDOM_URL = 'https://en.wikipedia.org/wiki/Special:Random'
LOCATION_URL_FORMAT = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=%d&gscoord=%lf|%lf&format=json'


def get_page_by_category(category: str) -> Article:
    """Gets the contents and metadata of a Wikipedia article with a given category.

    :param category: the category with which to search.
    :type category: str
    :returns: the Article object representing the Wikipedia article.

    """
    pass

def get_page_by_random() -> Article:
    """Gets the contents and metadata of a random Wikipedia article.
    
    :returns: the Article object representing the Wikipedia article.
    """

    page_html = None
    url = None
    while page_html is None:
        page_html, url = _get_page_and_url(RANDOM_URL)
    access_timestamp = int(time.time())

    article = _get_article_features(page_html, url, access_timestamp)
    return article

def get_page_by_location(latitude: float, longitude: float, radius: int) -> Article:
    """Gets the contents and metadata of a Wikipedia article close to the given coordinates.
    
    :param longitude: the longitude of the location, in decimal coordinates.
    :type longitude: float
    :param latitude: the latitude of the location, in decimal coordinates.
    :type latitude: float
    :param radius: the radius used to search, in meters.
    :type radius: int
    :returns: the Article object representing the Wikipedia article.
    """

    nearby_article_ids = _get_nearby_articles(latitude, longitude, radius)

    page_html = None
    url = None
    while page_html is None:
        nearby_article_id = random.choice(nearby_article_ids)
        page_html, url = _get_page_and_url(ARTICLE_BY_ID_URL + str(nearby_article_id))
    access_timestamp = int(time.time())

    article = _get_article_features(page_html, url, access_timestamp)
    return article
    pass

def _get_nearby_articles(latitude: float, longitude: float, radius: int) -> list:
    """Gets a list of Wikipedia articles that are located close to the given coordinates:
    
    :param longitude: the longitude of the location, in decimal coordinates.
    :type longitude: float
    :param latitude: the latitude of the location, in decimal coordinates.
    :type latitude: float
    :param radius: the radius used to search, in meters.
    :type radius: int
    :returns: a list of Wikipedia page ids.
    """
    req = None
    res = None
    try:
        url = LOCATION_URL_FORMAT % (radius, latitude, longitude)
        req = requests.get(url)
        res = json.loads(req.text)
        
    except ConnectionError:
        return None
    except requests.HTTPError:
        return None
    except requests.Timeout:
        return None

    #TODO add error handling for JSON.
    article_ids = [page['pageid'] for page in res['query']['geosearch']]
    
    return article_ids

def _get_page_and_url(url: str) -> (str, str):
    """Gets the HTML of a web page from a URL.

    :param url: the URL of the page from which to get the HTML.
    :type url: str
    :returns: the HTML and URL of the retrieved web page, or (None, None) if request fails.
    """
    req = None
    try:
        req = requests.get(url)

    except ConnectionError:
        return None, None
    except requests.HTTPError:
        return None, None
    except requests.Timeout:
        return None, None

    page_html = req.text
    if page_html is None or page_html == '':
        return None, None
    return page_html, req.url

def _get_article_features(page_html: str, url: str, access_timestamp: int) -> Article:
    """Parses the features of Article from the page html.

    :param page_html: the HTML of the page.
    :type page_html: str
    :param url: the URL of the page.
    :type url: str
    :param access_timestamp: the Unix timestamp at which the page was accessed.
    :type access_timestamp: int
    :returns: the Article object representing the Wikipedia page.
    """
    soup = bs4.BeautifulSoup(page_html, features="html.parser")
    content = ''
    for tag in soup.findAll('p'):
        content += ''.join(tag.strings) + '\n'

    categories = []
    categories_div = soup.find('div', {'id': 'mw-normal-catlinks'})
    for li in categories_div.ul.children:
        categories.append(li.text)

    long_span = soup.find('span', {'class': 'longitude'})
    lat_span = soup.find('span', {'class': 'latitude'})

    if long_span and lat_span:
        longitude = convert_dms_to_decimal(long_span.text)
        latitude = convert_dms_to_decimal(lat_span.text)
    else:
        longitude = None
        latitude = None

    article = Article(content, url, categories, access_timestamp, latitude, longitude)
    return article


def convert_dms_to_decimal(dms_coord: str) -> float:
    """Converts a degrees minutes seconds (DMS) coordinate to a decimal coordinate.
    
    :param dms_coord: a string representing a DMS coordinate.
    :type dms_coord: str
    :returns: a decimal coordinate.
    """
    try:
        dms = [0, 0, 0]
        delims = ['°', '′', '″']
        for i, delim in zip(range(len(dms)), delims):
            if delim in dms_coord:
                dms_coord = dms_coord.split(delim)
                dms[i] = int(dms_coord[0])
                dms_coord = dms_coord[1]
            else:
                dms[i] = 0

        degrees, minutes, seconds = dms
        # Set direction to 1 if North or East, else -1.
        direction = 1 if dms_coord[-1] in ['N', 'E'] else -1

        # DD = d + (min/60) + (sec/3600)
        decimal_coord = direction * (degrees + minutes / 60 + seconds / 3600)
        return decimal_coord
    except Exception as e:
        print(e, dms_coord)
        return None


if __name__ == '__main__':
    for _ in range(10):
        article = get_page_by_location(39.98, -75.16, 10000, )
        print(article, '\n')