import re ,os, hashlib ,sys
from urllib import request
from lxml import etree

__DIR__ = os.path.split(os.path.realpath(__file__))[0]

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
def getPage(url):
    req = request.Request(url)
    response = request.urlopen(req)
    html = response.read().decode('utf-8')
    return html

def md5(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()

def trimTitle(title):
    chars = [' ','-','_','/','\\','。','.','?','\'',':','，','(',')',' ','：','　']
    for char in chars :
        title = title.replace(char,'')
    return title

def getPageWithCache(url) :
    cacheFileName = '/tmp/py_get_'+md5(url)
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

def renderPost(post):
    global __DIR__
    filename = __DIR__ + '/template.md'
    md = Template(filename=filename)
    return md.render(**post)