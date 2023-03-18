# reference: https://www.scrapingbee.com/blog/crawling-python/

import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls

    def download_context(self, url):
        return requests.get(url).text

    def get_wanted_information(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        target_table = soup.select('center > table:nth-of-type(3)')[0]
        rows = target_table.select('tr')
        result = list()
        for index, row in enumerate(rows):
            if index not in [1, 2]:
                cells = row.select('td')
                result.append([cell.text.strip() for cell in cells])
        return result

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_context(url)
        contents = self.get_wanted_information(html)
        for content in contents:
            print(content)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

if __name__ == '__main__':
    Crawler(urls=['https://www.teaching.com.tw/member/case-list.php']).run()
