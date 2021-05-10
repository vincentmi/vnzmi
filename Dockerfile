
FROM ruby:2.7.3-slim-buster
LABEL  Author=miwenshu Site=http://vnzmi.com

ENV ALGOLIA_API_KEY=xxx

# 修改时区
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone

# 修改镜像
RUN  sed -i 's#http://deb.debian.org#http://mirrors.aliyun.com#g' /etc/apt/sources.list&& \
apt-get update && \
apt-get install -y ruby-full build-essential zlib1g-dev apt-utils && \
bundle config mirror.https://rubygems.org https://gems.ruby-china.com 
VOLUME /web
WORKDIR /web
COPY Gemfile Gemfile.lock /web/
# 加载插件
RUN  bundle install

EXPOSE  4000


#ENV  GEM_HOME=/usr/local/bundle PATH=/usr/local/bundle/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin


