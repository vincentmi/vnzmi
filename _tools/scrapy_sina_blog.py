# 
# 抓取新浪博客转换为Markdown博客
# 

from urllib import request
from lxml import etree
from bs4 import BeautifulSoup,NavigableString,Tag , Comment
import re ,os, hashlib ,sys
from datetime import datetime 
from mako.template import Template

__DIR__ = os.path.split(os.path.realpath(__file__))[0]

def getPage(url):
    req = request.Request(url)
    response = request.urlopen(req)
    html = response.read().decode('utf-8')
    return html

def getPageWithCache(url) :
    md5 = hashlib.md5()
    md5.update(url.encode('utf-8'))
    cacheFileName = '/tmp/py_get_'+md5.hexdigest()
    if(os.path.exists(cacheFileName)):
        fp = open(cacheFileName);
        html = fp.read()
        fp.close()
    else :
        html = getPage(url)
        fp = open(cacheFileName,'w')
        fp.write(html)
        fp.close()
    return html
def parseContent(url):
    html = getPageWithCache(url)
    #print(html)
    post = {}
    dom = BeautifulSoup(html,'lxml')
    titleElement = dom.select('#articlebody .articalTitle .titName')
    post['title'] = titleElement[0].text
    
    timeElement = dom.select('#articlebody .articalTitle .time')
    matcheObj = re.match('\((.*)\)',timeElement[0].text)
    timeStr = matcheObj.group(1)
    post['timestr'] = timeStr
    post['time'] = datetime.strptime(timeStr,'%Y-%m-%d %H:%M:%S')

    tags = dom.select('#articlebody .articalTag .blog_class a')
    post['tags'] = []
    for tag in tags :
        post['tags'].append(tag.text)

    body = dom.select('#articlebody .articalContent')
    bodytext=''
    Type_NavigableString = NavigableString('')
    for content in body[0].contents :
        if(content.__class__ == Type_NavigableString.__class__):
           bodytext += content
        else:
            print(content)

    post['body'] = bodytext
        
    return post
def renderPost(post):
    global __DIR__
    filename = __DIR__ + '/template.md'
    md = Template(filename=filename)
    return md.render(**post)

def downloadPicture(referer,url,toFile) : 
    req = request.Request(url)
    req.add_header('Referer',referer)
    response = request.urlopen(req)
    fp = open(toFile,'wb')
    fp.write(response.read())
    fp.close()
    return toFile

post = parseContent('http://blog.sina.com.cn/s/blog_542a39550100rqrm.html')
post['bg'] = 'life.jpg'
print(post)
exit(0)

print(renderPost(post))
downloadPicture(
    'http://blog.sina.com.cn/s/blog_542a39550100rqrm.html', 
    'http://s1.sinaimg.cn/middle/542a3955xa27f37f5ace0&amp;690',
    __DIR__+'/x.gif'
)


html = getPageWithCache('http://blog.sina.com.cn/vinz')
matched = re.search('\$uid\s*\:\s*\"([0-9]+)\"',html,re.S)
if(matched == None) :
    print('- 失败没有匹配到UID')
    exit(1)

uid = matched.group(1)

for i in range(1,10):
    url = 'http://blog.sina.com.cn/s/article_sort_'+uid+'_10001_'+str(i)+'.html'
    print(url)
    html = getPageWithCache(url)
    soup = BeautifulSoup(html,'lxml')
    articles = soup.select('.bloglist .blog_title a')
    for art in articles :
        print(" "+art.attrs['href'])