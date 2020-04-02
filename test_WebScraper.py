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

def test_remove_citations():
    original_expected_texts = [
        (
            """The American City Business Journals, which conducts a regular study to determine the most loyal fans in the NFL, evaluates fans based primarily on attendance-related factors,[82] and ranked Eagles fans third in both 1999[83] and 2006.[84] The 2006 study called the fans "incredibly loyal", noting that they filled 99.8% of the seats in the stadium over the previous decade.[85] Forbes placed the Eagles fans first in its 2008 survey,[86] which was based on the correlation between team performance and fan attendance.[87] ESPN.com placed Eagles fans fourth in the league in its 2008 survey, citing the connection between the team's performance and the mood of the city.[88] The last home game that was blacked out on television in the Philadelphia market as a result of not being sold out was against the Arizona Cardinals on Sunday, September 12, 1999, which was Andy Reid's first home game as new head coach of the Eagles.[citation needed]""",
            """The American City Business Journals, which conducts a regular study to determine the most loyal fans in the NFL, evaluates fans based primarily on attendance-related factors, and ranked Eagles fans third in both 1999 and 2006. The 2006 study called the fans "incredibly loyal", noting that they filled 99.8% of the seats in the stadium over the previous decade. Forbes placed the Eagles fans first in its 2008 survey, which was based on the correlation between team performance and fan attendance. ESPN.com placed Eagles fans fourth in the league in its 2008 survey, citing the connection between the team's performance and the mood of the city."""
        ),
        (
            """The name "Guinea" is of uncertain origin.[23] Residents in this area have been referred to as "Guineamen" at least since 1730, according to a tombstone inscription found by Brewton Berry (1963).[citation needed] As noted by George Dow in 1969, London physician George Pinckard referred to the master of a ship containing slaves from the Guinea coast as a "Guinea Man" in letters dating 1795.[citation needed] It is likely this area was called Guinea after being used as a landing site for importation of slaves from that area. Another story[2], passed among the "Guineamen" is that people on the Guinea Neck were continuing to use golden Guineas to pay for things up from about 1781–1860, the start of the American Civil War.[note 1][6]""",
            """The name "Guinea" is of uncertain origin. It is likely this area was called Guinea after being used as a landing site for importation of slaves from that area. Another story, passed among the "Guineamen" is that people on the Guinea Neck were continuing to use golden Guineas to pay for things up from about 1781–1860, the start of the American Civil War."""
        )
    ]

    for original, expected in original_expected_texts:
        processed_text = remove_citations(original)
        assert processed_text == expected