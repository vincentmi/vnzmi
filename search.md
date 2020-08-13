---
layout: page
title: 搜索
permalink: /search/
header-img: "img/post-b1.jpg"
---


<div id="search-searchbar"></div>
<div id="search-hits"></div>


<script src="https://cdn.jsdelivr.net/npm/instantsearch.js@2.6.0/dist/instantsearch.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/moment@2.20.1/moment.min.js"></script>
<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/instantsearch.js@2.6.0/dist/instantsearch.min.css">
<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/instantsearch.js@2.6.0/dist/instantsearch-theme-algolia.min.css">

<script>
const search = instantsearch({
  appId: '{{ site.algolia.application_id }}',
  apiKey: '{{ site.algolia.search_only_api_key }}',
  indexName: '{{ site.algolia.index_name }}'
});
search.urlSync = true


const hitTemplate = function(hit) {
  let date = '';
  if (hit.date) {
    date = moment.unix(hit.date).format('MM/DD/YYYY');
  }

  let url = `{{ site.baseurl }}${hit.url}#${hit.anchor}`;

  const title = hit._highlightResult.title.value;

  let breadcrumbs = '';
  if (hit._highlightResult.headings) {
    breadcrumbs = hit._highlightResult.headings.map(match => {
      return `<span class="post-breadcrumb">${match.value}</span>`
    }).join(' > ')
  }

  const content = hit._highlightResult.html.value.trim();

  return `
    <div class="post-item">
      <h2><a class="post-link" href="${url}">${title}</a></h2>
      <div class="post-snippet">${content}</div>
      <span class="post-meta">${date}</span>
    </div>
  `;
}


search.addWidget(
  instantsearch.widgets.searchBox({
    container: '#search-searchbar',
    placeholder: '输入关键字',
    poweredBy: true // This is required if you're on the free Community plan
  })
);

search.addWidget(
  instantsearch.widgets.hits({
    container: '#search-hits',
    templates: {
      item: hitTemplate
    }
  })
);

search.start();

</script>

<style>
.ais-search-box {
  max-width: 90%;
  margin-bottom: 15px;
}
.post-item {
  margin-bottom: 30px;
}
.post-link .ais-Highlight {
  color: red;
  font-style: normal;

  text-decoration: none;
}
.post-breadcrumbs {
  color: #424242;
  display: block;
}
.post-breadcrumb {
  font-size: 18px;
  color: #424242;
}
.post-breadcrumb .ais-Highlight {
  font-weight: bold;
  font-style: normal;
}
.post-snippet .ais-Highlight {
  color: red;
  font-style: normal;
}

.post-snippet img {
  display: none;
}
</style>