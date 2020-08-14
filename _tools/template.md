---
layout:     post
title:      "${title}"
date:       ${timestr}
author:     "Vincent"
header-img:  "img/${bg}.jpg"
catalog: true
tags:
    % for tag in tags:
    - ${tag}
    % endfor
---

${body}