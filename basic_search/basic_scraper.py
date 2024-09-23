from duckduckgo_search import DDGS
from duckduckgo_search import AsyncDDGS
import logging
from unstructured.partition.html import partition_html
import threading
from queue import Queue

class BasicScraper:
    def __init__(
            self,
            blacklist = [],
            whitelist = []
        ):
        """
        Args:
            blacklist (array): Blacklisted websites, defaults to an empty list (Results from all websites)
            whitelist (int): Whitelisted websites (Results shown are only from this list), defaults to an empty list (Results from all websites)
        """
        self.blacklist = blacklist
        self.whitelist = whitelist

    def scrapeUrl(self, url, queue):
        elements = partition_html(url=url, headers={"User-Agent": "value"})
        content = ""
        for element in elements:
            content += str(element)
        
        queue.put({url: content})

    def queueScraping(self, urls):
        logging.debug('Starting Scraping')
        threads = []
        queue = Queue()
        json_content = []
        for url in urls:
            thread = threading.Thread(target=self.scrapeUrl, args=(url, queue))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        while not queue.empty():
            json_content.append(queue.get())

        return json_content

    def syncBasicTextSearch(self, query: str, results: int = 5):
        logging.debug('Starting Sync Search')
        sources = []
        code = 503
        try:
            if query:
                logging.debug('Query was received')
                code = 200
                if len(self.whitelist) > 0:
                    logging.debug("Whitelisting")
                    for url in self.whitelist:
                        query += " " + url

                if len(self.blacklist) > 0:
                    logging.debug('Blacklisting')
                    query += " -"
                    for url in self.blacklist:
                        query += f"{url}"

                
                logging.debug(f"Final Query : {query}")
            
                sources = DDGS().text(query, max_results=results)
            else:
                logging.debug('Query was empty or null')
                raise Exception('Query was empty or null')
        except Exception as e:
            logging.error(f'Exception caught : {e}')
            code = 503; sources = []
        finally:
            return {"code": code, "sources": sources}

    async def asyncBasicTextSearch(self, query: str, results: int = 5):
        logging.debug('Starting Async Search')
        sources = []
        code = 503
        try:
            if query:
                logging.debug('Query was received')
                code = 200
                if len(self.whitelist) > 0:
                    for url in self.whitelist:
                        query += " " + url

                if len(self.blacklist) > 0 and len(self.whitelist) == 0:
                    query += " -"
                    for url in self.blacklist:
                        query += " " + url

                sources = await AsyncDDGS().atext(query, max_results=results)
            else:
                logging.debug('Query was empty or null')
                raise Exception('Query was empty or null')
        except Exception as e:
            logging.error(f'Exception caught : {e}')
            code = 503; sources = []
        finally:
            return {"code": code, "sources": sources}