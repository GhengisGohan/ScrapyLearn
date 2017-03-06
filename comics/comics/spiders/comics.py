# -*- coding: utf-8 -*-

# 创建:scrapy startproject comics
# 运行:scrapy crawl comics
# 存储数据:scrapy crawl dmoz -o items.json

import scrapy
import os
import zlib
import urllib
from bs4 import BeautifulSoup


class Comics(scrapy.Spider):
    name = "comics"

    def start_requests(self):
        urls = ['http://www.xeall.com/shenshi']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # 负责解析返回的数据并提取
    def parse(self, response):
        # 请求返回html源码
        content = response.body
        if not content:
            self.log('parse body error')
            return
        # 进行节点解析
        soup = BeautifulSoup(content, 'html5lib')

        # 获取漫画列表标签
        listcon_tag = soup.find('ul', class_='listcon')
        if len(listcon_tag) < 1:
            self.log('extract comics list error')
            return

        # 列表中每个漫画<a>标签
        com_a_list = listcon_tag.find_all('a', attrs={'href': True})
        if len(listcon_tag) < 1:
            self.log('can not find <a> that contain href attribute')
            return

        # 获取列表中漫画url
        comics_url_list = []
        base = 'http://www.xeall.com'
        for tag_a in com_a_list:
            url = base + tag_a['href']
            comics_url_list.append(url)
        print('\n>>>>>>>> current page comics list <<<<<<<<')
        print(comics_url_list)

        # 处理当前页漫画
        for url in comics_url_list:
            print('>>>>>>>> parse comics: ' + url)
            yield scrapy.Request(url=url, callback=self.comics_parse)

        # 漫画列表下方选页栏
        page_tag = soup.find('ul', class_='pagelist')
        if len(page_tag) < 1:
            self.log('extract page list error')
            return

        # 获取下一页url
        page_a_list = page_tag.find_all('a', attrs={'herf': True})
        if len(page_a_list) < 2:
            self.log('extract page tag a error')
            return

        # 判断是否为最后一页
        select_tag = soup.find('select', attrs={'name': 'sldd'})
        option_list = select_tag.find_all('option')

        last_option = option_list[-1]
        current_option = select_tag.find('option', attrs={'selected': True})
        is_list = (last_option.string == current_option.string)

        if not is_list:
            next_page = 'http://www.xeall.com/shenshi/' + \
                page_a_list[-2]['href']
            if next_page is not None:
                print('\n-------- parse next page --------')
                print(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
                pass
        else:
            print('======== last page ========')

    def comics_parse(self, response):
        content = response.body
        if not content:
            self.log('parse comics body error')
            return
        soup = BeautifulSoup(content, 'html5lib')

        # 选择页控件标签
        page_list_tag = soup.find('ul', class_='pagelist')

        # 当前页数
        current_li = page_list_tag.find('li', class_='thisclass')
        page_num = current_li.a.string
        self.log('current page = ' + page_num)

        # 显示当前页图片标签
        li_tag = soup.find('li', id='imgshow')
        img_tag = li_tag.find('img')

        # 当前图片url
        img_url = img_tag['src']
        self.log('img url: ' + img_url)

        # 漫画标题
        title = img_tag['alt']

        # 保存图片
        self.save_img(page_num, title, img_url)
        a_tag_list = page_list_tag.find_all('a')
        next_page = a_tag_list[-1]['href']
        if next_page == '#':
            self.log('parse comics:' + title + 'finished')
        else:
            next_page = 'http://www.xeall.com/shenshi/' + next_page
            yield scrapy.Request(next_page, callback=self.comics_parse)

    def save_img(self, img_num, title, img_url):
        self.log('saving pic: ' + img_url)
        document = '/Users/admin/Documents/sample'

        comics_path = document + '/' + title
        exists = os.path.exists(comics_path)
        if not exists:
            self.log('create document: ' + title)
            os.makedirs(comics_path)

        pic_name = comics_path + '/' + img_num + '.jpg'

        exists = os.path.exists(pic_name)
        if exists:
            self.log('pic exists: ' + pic_name)
            return

        try:
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = {'User-Agent': user_agent}

            req = urllib.request.Request(img_url, headers=headers)
            response = urllib.request.urlopen(req, timeout=30)

            data = response.read()
            if response.info().get('Content-Encoding') == 'gzip':
                data = zlib.decompress(data, 16 + zlib.MAX_WBITS)

            fp = open(pic_name, 'wb')
            fp.write(data)
            fp.close

            self.log('save image finished: ' + pic_name)
        except Exception as e:
            self.log('save image error')
            self.log(e)
