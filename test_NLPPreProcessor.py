from trivia_generator.web_scraper import WebScraper
from trivia_generator import NLPPreProcessor
from trivia_generator import TUnit

# TODO make actual unit tests for NLPPreProcessor

print('Getting Article object...')
article = WebScraper.get_page_by_random()
print('Creating TUnits...')
tunits = NLPPreProcessor.create_TUnits(article)
print('Retrieved', len(tunits), 'TUnits from article.')
TUnit.tunit_list_to_tsv(tunits)
print('TUnits written to TSV file.')