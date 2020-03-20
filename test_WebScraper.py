import math

from trivia_generator.web_scraper.WebScraper import *

def test_get_page_by_location():
    # Search 10km around Temple University, Philadelphia, PA.
    latitude = 39.98
    longitude = -75.16
    dist = 10000

    # Get an article using those parameters, and test whether the resulting article is
    # 10km or closer to the original point.
    article = get_page_by_location(latitude, longitude, dist)
    article_dist = math.hypot(article.latitude - latitude, article.longitude - longitude)
    assert article_dist <= dist

def test_get_page_by_location_with_invalid_coordinates():
    latitude = 43927
    longitude = 69420
    dist = 10000

    article = get_page_by_location(latitude, longitude, dist)
    assert article is None

def test_get_page_by_random():
    article = get_page_by_random()
    assert article is not None

def test_get_page_by_category():
    category_name = "People by status"
    article = get_page_by_category(category_name)
    assert category_name in article.categories

def test_get_page_by_category_with_invalid_category():
    category_name = "gaeigjeklgj"
    article = get_page_by_category(category_name)
    assert article is None

def test_convert_dms_to_decimal():
    dms_test_suite = [
        ("38°43′31″N", 38.725),
        ("9°09′00″W", -9.150),
        ("38°43′31″S", -38.725),
        ("9°09′00″E", 9.150),
        ("38°43′N", 38.717),
        ("9°00″W", -9),
        ("30′30″W", -0.508),
    ]
    for dms, decimal in dms_test_suite:
        test_decimal = round(convert_dms_to_decimal(dms), 3)
        assert decimal == test_decimal