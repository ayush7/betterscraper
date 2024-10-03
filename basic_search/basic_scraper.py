from duckduckgo_search import DDGS
import logging
import threading
from queue import Queue
from crawl4ai.web_crawler import WebCrawler

from pathlib import Path 
import os 
import time

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

    def scrape_url(self, url, queue, logging = False, logs_dir='logs'):
        
        try:
            result = self.crawler.run(url=url)
        except Exception as e:
            print(f'\nException in link {url}')
            if logging == True:
                Path(logs_dir).mkdir(parents=True, exist_ok=True)
                timestr = time.strftime("%Y%m%d")
                log_path = os.path.join(logs_dir,'exception_logs_scraper_'+timestr+'.txt')
                with open(log_path,'a') as f:
                    f.write(f'\nLink: {url}\nException: {str(e)}\n')
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

    def basic_text_search(self, query: str, results: int = 5):
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
