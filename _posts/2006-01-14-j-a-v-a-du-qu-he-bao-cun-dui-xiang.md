---
layout:     post
title:      "java读取和保存对象"
date:       2006-01-14 12:26:43
author:     "Vincent"
header-img:  "img/post-bg-dot.jpg"
catalog: false
tags:
    - 新浪博客
    - 技术文章
---




有这个东西，做缓存就很方便了

```java
Map map = new HashMap();
FileOutputStream fos = new FileOutputStream("d:\\111.conf");
ObjectOutputStream o = new ObjectOutputStream(fos);
o.writeObject(map);
fos.close();
o.close();
FileInputStream fis = new FileInputStream(new File("d:\\111.conf"));
ObjectInputStream ois = new ObjectInputStream(fis);
Map map = (Map)ois.readObject();
System.out.println(map.size());
fis.close();
ois.close();
```



