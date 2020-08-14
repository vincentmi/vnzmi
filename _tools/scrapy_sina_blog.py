# 
# 抓取新浪博客转换为Markdown博客
# 

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

__DIR__ = os.path.split(os.path.realpath(__file__))[0]

__POST_FOLDER__ = __DIR__+'/../_posts/'
__POST_IMG__ = __DIR__+'/../img/sinablog/'

__SKIP__URLS = ['http://blog.sina.com.cn/s/blog_542a3955010001mp.html',
'http://blog.sina.com.cn/s/blog_542a39550100003i.html',
'http://blog.sina.com.cn/s/blog_542a3955010001jy.html',
'http://blog.sina.com.cn/s/blog_542a3955010001wu.html']

def getPage(url):
    req = request.Request(url)
    response = request.urlopen(req)
    html = response.read().decode('utf-8')
    return html

def trimTitle(title):
    chars = [' ','-','_','/','\\','。','.','?','\'',':','，','(',')',' ','：','　']
    for char in chars :
        title = title.replace(char,'')
    return title

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
    global __POST_IMG__
    html = getPageWithCache(url)
    #print(html)
    post = {}
    dom = BeautifulSoup(html,'lxml')
    titleElement = dom.select('#articlebody .articalTitle .titName')
    if len(titleElement) == 0 :
        #print(html)
        return ""
    title = titleElement[0].text
    post['title'] = title
    post['source'] = url
    post['title_pinyin'] = pinyin.get(trimTitle(title),format="strip", delimiter="-")
    
    timeElement = dom.select('#articlebody .articalTitle .time')
    matcheObj = re.match('\((.*)\)',timeElement[0].text)
    timeStr = matcheObj.group(1)
    post['timestr'] = timeStr
    
    postCreatedAt = datetime.strptime(timeStr,'%Y-%m-%d %H:%M:%S')
    post['time'] = postCreatedAt
    post['timeymd'] = postCreatedAt.strftime('%Y-%m-%d')

    tags = dom.select('#articlebody .articalTag .blog_class a')
    post['tags'] = ['新浪博客']
    for tag in tags :
        post['tags'].append(tag.text)

    body = dom.select('#articlebody .articalContent')
    bodytext=''
    Type_NavigableString = NavigableString('')
    Type_Comment = Comment('')
    for content in body[0].contents :
        if(content.__class__ == Type_NavigableString.__class__):
           bodytext += str(content).strip()+"\n"
        elif (content.__class__ == Type_Comment.__class__ ) :
            bodytext += content
        else:
            if content.name == 'br' :
                bodytext += "\n"
            else:
                
                imgs = content.select('img')
                bodytextTemp = ''
                for img in imgs:
                    imgUrl=img.attrs['real_src']
                    md5 = hashlib.md5()
                    md5.update(imgUrl.encode('utf-8'))
                    imgNewName = md5.hexdigest()
                    tempFile = '/tmp/'+imgNewName
                    newFile = __POST_IMG__+imgNewName
                    relateFile = '/img/sinablog/'+imgNewName
                    if downloadPicture(url,imgUrl,tempFile) == 1 :
                        imgType = imghdr.what(tempFile)
                        if imgType is not None :
                            #shutil.move(tempFile,newFile+'.'+imgType)
                            relateFile = relateFile + '.'+imgType
                            bodytextTemp+="!["+relateFile+"]("+relateFile+")\n"
                bodytext+= bleach.clean(str(content), tags=['img'], strip=True)+"\n" + bodytextTemp
    post['body'] = bodytext
        
    return post
def renderPost(post):
    global __DIR__
    filename = __DIR__ + '/template.md'
    md = Template(filename=filename)
    return md.render(**post)

def downloadPicture(referer,url,toFile) : 
    try:
        req = request.Request(url)
        req.add_header('Referer',referer)
        response = request.urlopen(req)
        if response.getcode() == 200 :
            fp = open(toFile,'wb')
            fp.write(response.read())
            fp.close()
            return 1
        return 0
    except BaseException:
        return 0
    else:
        return 1 

html = getPageWithCache('http://blog.sina.com.cn/vinz')
matched = re.search('\$uid\s*\:\s*\"([0-9]+)\"',html,re.S)
if(matched == None) :
    print('- 失败没有匹配到UID')
    exit(1)

uid = matched.group(1)

for i in range(1,10):
    url = 'http://blog.sina.com.cn/s/article_sort_'+uid+'_10001_'+str(i)+'.html'
    print("PAGE - " + url)
    html = getPageWithCache(url)
    soup = BeautifulSoup(html,'lxml')
    articles = soup.select('.bloglist .blog_title a')
    for art in articles :
        postUrl = art.attrs['href']
        print("     -> "+postUrl)
        if postUrl in __SKIP__URLS :
            continue
        post = parseContent(postUrl)
        if post != "" :
            post['bg'] = 'xinyuan-no7.jpg'
            postMd = (renderPost(post))
            fp = open(__POST_FOLDER__+post['timeymd']+'-'+post['title_pinyin']+'.md','w+')
            fp.write(postMd)
            fp.close()
        else:
            print("     x- NO Title ")