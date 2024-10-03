from duckduckgo_search import DDGS
from duckduckgo_search import AsyncDDGS
import logging
import threading
from queue import Queue
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.web_crawler import WebCrawler

class BasicScraper:
    
    def __init__(
            self,
            blacklist = [],
            whitelist = [],
            crawler = None
        ):
        """
        Args:
            blacklist (array): Blacklisted websites, defaults to an empty list (Results from all websites)
            whitelist (int): Whitelisted websites (Results shown are only from this list), defaults to an empty list (Results from all websites)
            crawler (crawl4ai.web_crawler) : Crawler Object from Crawl4AI to scrape websites for content
        """
        self.blacklist = blacklist
        self.whitelist = whitelist
        if not crawler:
            self.crawler = WebCrawler()
            self.crawler.warmup()

    async def ascrape_url(self, url, queue):
        async with AsyncWebCrawler(verbose=True) as crawler:
            result = await crawler.arun(url=url)
            queue.put({url: result.markdown})

    def queue_scraping(self, urls):
        logging.debug('Starting Scraping')
        threads = []
        queue = Queue()
        json_content = []
        for url in urls:
            thread = threading.Thread(target=self.scrape_url, args=(url, queue))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        while not queue.empty():
            json_content.append(queue.get())

        return json_content

    async def abasic_text_search(self, query: str, results: int = 5):
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