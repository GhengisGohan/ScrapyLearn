import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from lianjia.items import LianjiaItem
import requests
import re


class myspider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['sh.lianjia.com']

    def start_requests(self):
        theme_url = 'http://sz.lianjia.com/zufang/luohuqu/pg1/'
        html = requests.get(theme_url)
        content = BeautifulSoup(html.text, 'lxml')

        urls = []
        links = content.find(
            'div', class_='option-list').find_all('a')
        for link in links:
            i = re.findall(r'g/(.*)/', link['href'])
            if i:
                urls.extend(i)
        # 构造出每一个区域的链接
        all_url = ['http://sz.lianjia.com/zufang/{}/pg1/'.format(i) for i in urls]
        for url in all_url:
            print(url)
            yield Request(url, self.parse)

    def parse(self, response):
        page = BeautifulSoup(response.text, 'lxml').find(
            'div', class_='page-box house-lst-page-box')
        max_page = re.findall('Page":(\d+)."cur', str(page))[0]
        bashurl = str(response.url)[:-2]
        for num in range(1, int(max_page) + 1):
            url = bashurl + str(num) + '/'
            # print(url)
            yield Request(url, callback=self.get_message)

    def get_message(self, response):
        item = LianjiaItem()
        content = BeautifulSoup(response.text, 'lxml')

        house_list = content.find_all(
            'div', {'class': 'info-panel'})

        for li in house_list:
            try:
                data = li.find(
                    'span', class_='fang-subway-ex').find('span').get_text()
                item['distance'] = re.findall(
                    r'(\d+)', data)[1]
            except:
                item['distance'] = "没有附近地铁数据"
            try:
                item['year_build'] = re.findall(
                    r'(\d+)', li.find('div', class_='con').get_text().split('/')[-1])[0]
            except:
                item['year_build'] = '没有建造年份'
                item['title'] = li.find('h2').find('a').attrs['title']
                item['rental'] = li.find(
                    'div', class_='price').find('span').get_text()
                item['area'] = re.findall(
                    r'(\d+)', li.find('span', class_='meters').get_text().replace('&nbsp', ''))[0]
                item['room_number'] = li.find('span', class_='zone').find(
                    'span').get_text().replace('\xa0', '')
                item['floor'] = li.find(
                    'div', class_='con').get_text().split('/')[1]
                item['direction'] = li.find(
                    'div', class_='where').find_all('span')[-1].get_text()
            yield item
