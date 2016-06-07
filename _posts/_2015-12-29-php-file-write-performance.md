---
layout:     post
title:      "PHP 文件写性能比较"
date:       2015-12-29 23:49:00
author:     "Vincent"
header-img:  "img/post-bg.jpg"
catalog: true
tags:
    - RD
    - PHP
---

最近项目需要用到PHP收集日志，需要一个驻留程序进行大量的文件写入，进行了一些测试

以下几种方式
- 打开文件持续写入，不关闭文件
- 打开文件写入然后关闭
- 打开文件锁定写入解锁，不关闭
- file_put_contents 

使用以上方式写入10000行随机文本，代码如下

```php
    <?php
    $lines = files('data.txt');
    $fp = fopen("out",'a');
    foreach($lines as $line)
    {
        fwrite($fp,$line);
    }
    fclose($fp);
```




