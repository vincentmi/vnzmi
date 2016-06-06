---
layout:     post
title:      "Apache option选项"
date:       2015-05-03 8:36:00
author:     "Vincent"
header-img:  "img/post-bg.jpg"
catalog: true
tags:
    - 运维
---
Options指令控制了在特定目录中将使用哪些服务器特性。

option可以为None，在这种情况下，将不启用任何额外特性。或设置为以下选项中的一个或多个：

All除MultiViews之外的所有特性。这是默认设置。ExecCGI允许使用 mod_cgi执行CGI脚本。FollowSymLinks服务器允许在此目录中使用符号连接。      
注意：即使服务器会使用符号连接，但它不会改变用于匹配<Directory>段的路径名。

注意：如果此配置位于<Location>配置段中，则此设置会被忽略。