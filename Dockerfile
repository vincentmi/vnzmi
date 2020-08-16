FROM  jekyll/jekyll:3.8

LABEL author=vincentmi

ENV ALGOLIA_API_KEY=xxx

RUN  echo  http://mirrors.aliyun.com/alpine/v3.10/main/ > /etc/apk/repositories \
 && apk add tzdata \ 
 && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
 && echo "Asia/Shanghai" > /etc/timezone \
 && gem sources --add https://mirrors.tuna.tsinghua.edu.cn/rubygems/ --remove https://rubygems.org/

RUN  gem install jekyll-algolia jekyll-paginate

