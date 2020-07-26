export JEKYLL_VERSION=3.8
docker run --rm \
  -p 4000:4000 \
  --volume="$PWD:/srv/jekyll" \
  --volume="$PWD/vendor/bundle:/usr/local/bundle" \
  -it jekyll/jekyll:$JEKYLL_VERSION \
  jekyll serve

#docker run --rm  -v `pwd`:/srv/jekyll -e "ALGOLIA_API_KEY=b371ed94299fc01422c1ab5c7bbd39e1"  jk  ./update_index.sh

  # docker run -d  -v `pwd`:/srv/jekyll -v `pwd`/vendor/bundle:/usr/local/bundle jk jekyll serve 