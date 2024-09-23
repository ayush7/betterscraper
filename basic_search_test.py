from basic_search import *
import logging
logging.basicConfig(level=logging.DEBUG)
import json
# query rewriter
basicSearch = BasicScraper(blacklist=['site:instagram.com'], whitelist=[])

results = basicSearch.syncBasicTextSearch("Gemini Flash 1.5", 10)

urls = []

for data in results['sources']:
    urls.append(data['href'])

print(json.dumps(basicSearch.queueScraping(urls), indent=4))
