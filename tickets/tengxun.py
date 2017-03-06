#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import re

print('https://v.qq.com/x/cover/g4y2d81zw85x9f8/e0022d9gfyi.html')
web = input('Input URL:\n')
# 从视频页面获取VID
if re.search(r'vid=', web):
    patten = re.compile(r'vid=(.*)')
    vid = patte.findall(web)
    vid = vid[0]
else:
    newurl = (web.split('/')[-1])
    vid = newurl.replace('.html', ' ')

# 打开网页的函数
def getpage(url):
    req = Request(url)
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit'
    req.add_header('User-Agent', user_agent)
    try:
        response = urlopen(url)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code:', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason:', e.reason)
    html = response.read().decode('utf-8')
    return(html)

getinfo = 'https://vv.video.qq.com/getinfo?vids={vid}  \
           &defaultfmt=auto&otype=json'.format(vid=vid.strip())
a = getpage(getinfo)
print(a)

# 找到ID和拼接FILENAME
soup = BeautifulSoup(a, 'html.parser')
for e1 in soup.find_all('url'):
    ippattent = re.compile(
        r'((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))')
    if re.search(ippattent, e1.get_text()):
        ip = (e1.get_text())
for e2 in soup.find_all('id'):
    idpattent = re.compile(r'\d{5}')
    if re.search(idpattent, e2.get_text()):
        id = (e2.get_text())
filename = vid.strip() + '.p' + id[2:] + '.2.mp4'
print(filename)

# 利用getinfo中的信息拼接getkey网址
getkey = 'http://vv.video.qq.com/getkey?format={id}&charge=0&vid={vid}&otype=json\
          &filename={filename}&platform=10901'.format(id=id, vid=vid.strip(), filename=filename)
b = getpage(getkey)
print(b)

key = (re.findall(r'<key>(.*)<\\\\/key>', b))
videourl = ip + filename + '?' + 'vkey=' + key[0]
print('Open URL:\n' + videourl)
