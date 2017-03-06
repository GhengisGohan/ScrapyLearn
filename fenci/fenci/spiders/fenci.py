import scrapy
from bs4 import BeautifulSoup
from fenci.items import FenciItem


class Fenci(scrapy.Spider):
    name = 'fenci'
    n = 0

    def start_requests(self):
        start_url = [
            'http://www.360doc.com/content/16/1026/12/34624569_601474728.shtml']
        for url in start_url:
            yield scrapy.Request(url=url, callback=self.parse_getlink)

    def parse_getlink(self, response):
        n = 0
        soup = BeautifulSoup(response.body, 'lxml')
        for i in soup.find_all('td', id='artContent'):
            for j in i.find_all('a'):
                url = j.get('href')
                yield scrapy.Request(url=url, callback=self.parse)
                n = n + 1
        print(n)

    def parse(self, response):
        item = FenciItem()
        soup = BeautifulSoup(response.body, 'lxml')
        for i in soup.find_all('div', id='js_content'):
            item['content'] = i.get_text()
            yield item
