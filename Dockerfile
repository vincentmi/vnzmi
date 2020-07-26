FROM  jekyll/jekyll:3.8

LABEL author=vincentmi

ENV ALGOLIA_API_KEY=xxx

RUN  gem sources --add https://gems.ruby-china.com/ --remove https://rubygems.org/ && gem install jekyll-algolia && gem install jekyll-paginate

