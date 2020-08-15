from urllib import request
from lxml import etree
from bs4 import BeautifulSoup,NavigableString,Tag , Comment
import re ,os, hashlib ,sys
from datetime import datetime 
from mako.template import Template
import pinyin
import imghdr
import shutil
import bleach
from util import downloadPicture,getPage,trimTitle,getPageWithCache,md5,renderPost

__DIR__ = os.path.split(os.path.realpath(__file__))[0]
__POST_FOLDER__ = __DIR__+'/../_posts/'
__POST_IMG__ = __DIR__+'/../img/poco/'

postUrls = [
    'https://wap.poco.cn/works/detail_id1107262',
    'https://wap.poco.cn/works/detail_id979599',
    'https://wap.poco.cn/works/detail_id807653',
    'https://wap.poco.cn/works/detail_id754518',
    'https://wap.poco.cn/works/detail_id749192',
    'https://wap.poco.cn/works/detail_id747925',
    'https://wap.poco.cn/works/detail_id742151',
    'https://wap.poco.cn/works/detail_id732533',
    'https://wap.poco.cn/works/detail_id720669'
]
url = postUrls[0]
html = getPageWithCache(url)
dom = BeautifulSoup(html,'lxml')
items = dom.select('#base_works_detail img')

# print(items)
for item in items:
    
    if 'data-src' in item.attrs.keys() :
        picUrl = 'http:'+item.attrs['data-src']
        print(picUrl)
        file = md5(picUrl)
        downloadPicture(url,picUrl,'/tmp/'+file+'.jpg')
        shutil.move('/tmp/'+file+'.jpg',__POST_IMG__+file+'.jpg')

#print(items)