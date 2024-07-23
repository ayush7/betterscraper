from duckduckgo_search import DDGS
from duckduckgo_search import AsyncDDGS
import logging

def syncBasicSearch(query: str, results: int = 5):
    logging.debug('Starting Sync Search')
    sources = []
    code = 503
    try:
        if query:
            logging.debug('Query was received')
            code = 200
            sources = DDGS().text(query, max_results=results)
        else:
            logging.debug('Query was empty or null')
            raise Exception('Query was empty or null')
    except:
        logging.error(f'Exception caught : {e}')
        code = 503; sources = []
    finally:
        return {"code": code, "sources": sources}

async def asyncBasicSearch(query: str, results: int = 5):
    logging.debug('Starting Async Search')
    sources = []
    code = 503
    try:
        if query:
            logging.debug('Query was received')
            code = 200
            sources = await AsyncDDGS().atext(query, max_results=results)
        else:
            logging.debug('Query was empty or null')
            raise Exception('Query was empty or null')
    except:
        logging.error(f'Exception caught : {e}')
        code = 503; sources = []
    finally:
        return {"code": code, "sources": sources}