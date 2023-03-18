# reference: https://www.scrapingbee.com/blog/crawling-python/

import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO,
)

class Crawler:

    def __init__(self, url=None):
        self.url_to_visit = url

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

    def crawl(self, url):
        html = self.download_context(url)
        contents = self.get_wanted_information(html)
        results = [{
            'id': content[0],
            'student': content[1],
            'city': content[2],
            'location': content[3],
            'subject': content[4],
            'time': content[5],
        } for index, content in enumerate(contents) if index != 0]
        return results

    def run(self):
        url = self.url_to_visit
        logging.info(f'Crawling: {url}')
        try:
            results = self.crawl(url)
            return results
        except Exception:
            logging.exception(f'Failed to crawl: {url}')
            return []
