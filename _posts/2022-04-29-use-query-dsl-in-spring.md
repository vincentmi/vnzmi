---
layout:     post
title:      "使用Querydsl简化Spring JPA的查询"
date:       "2022-04-29 22:55:00"
author:     "Vincent"
header-img:  "img/leaf.jpg"
catalog: true
tags:
    - springboot
    - Java
    - spring
    - Querydsl
---

## JPA的限制

一般项目中一定会使用到联表查询,使用JPA可以很方便的对单表进行CRUD操作,简单的关联操作通过设置关联关系也很容易实现.但是对于多表的联合查询就比较麻烦.使用Querydsl可以帮助我们很方便的构建复杂查询.

## MAVEN依赖

添加依赖 

```xml
<dependency>
  <groupId>com.querydsl</groupId>
  <artifactId>querydsl-apt</artifactId>
  <version>${querydsl.version}</version>
  <scope>provided</scope>
</dependency>

<dependency>
  <groupId>com.querydsl</groupId>
  <artifactId>querydsl-jpa</artifactId>
  <version>${querydsl.version}</version>
</dependency>
```

添加MAVEN APT插件

```xml
<plugin>
      <groupId>com.mysema.maven</groupId>
      <artifactId>apt-maven-plugin</artifactId>
      <version>1.1.3</version>
      <executions>
        <execution>
          <goals>
            <goal>process</goal>
          </goals>
          <configuration>
            <outputDirectory>target/generated-sources/java</outputDirectory>
            <processor>com.querydsl.apt.jpa.JPAAnnotationProcessor</processor>
          </configuration>
        </execution>
      </executions>
    </plugin>
```


