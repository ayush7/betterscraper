from basic_search import *
import logging
logging.basicConfig(level=logging.DEBUG)
import json

basicSearch = BasicScraper()

# results = basicSearch.basic_text_search("Gemini Flash 1.5", 10)

urls = ["https://deepmind.google/technologies/gemini/flash/"]

# for data in results['sources']:
#     urls.append(data['href'])

print(json.dumps(basicSearch.queue_scraping(urls)))
