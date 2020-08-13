#!/bin/sh

cd /alidata/www/vnzmi

git pull

#docker run --rm   -v /alidata/www/vnzmi:/srv/jekyll  jekyll/builder:3.7.0 jekyll build --trace
docker run --rm -v /alidata/www/vnzmi:/srv/jekyll  -v /alidata/www/vnzmi/vendor/bundle:/usr/local/bundle -e "ALGOLIA_API_KEY=$ALGOLIA_API_KEY" jk ./update_index.sh