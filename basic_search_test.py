from basic_search import *
import logging
logging.basicConfig(level=logging.DEBUG)

results = syncBasicSearch("Hello", 6)

print(results)