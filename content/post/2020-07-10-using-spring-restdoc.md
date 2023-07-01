---
layout:     post
title:      "使用Spring REST Docs生成项目API文档"
date:       "2020-07-10 09:55:00"
author:     "Vincent"
image:  "img/post-bg-info.jpg"
catalog: true
tags:
    - Spring
    - RESTFul
    - Swagger
---

# 配置依赖

## 增加依赖 ```pom.xml```
```xml
<dependency>
        <groupId>org.springframework.restdocs</groupId>
        <artifactId>spring-restdocs-mockmvc</artifactId>
</dependency>
```

##  添加Maven插件
```xml
<plugin>
    <groupId>org.asciidoctor</groupId>
    <artifactId>asciidoctor-maven-plugin</artifactId>
    <version>1.5.8</version>
    <executions>
        <execution>
            <id>generate-docs</id>
            <phase>prepare-package</phase>
            <goals>
                <goal>process-asciidoc</goal>
            </goals>
            <configuration>
                <backend>html</backend>
                <doctype>book</doctype>
            </configuration>
        </execution>
    </executions>
    <dependencies>
        <dependency>
            <groupId>org.springframework.restdocs</groupId>
            <artifactId>spring-restdocs-asciidoctor</artifactId>
        </dependency>
    </dependencies>
</plugin>
```

##  如果要将文档打入Jar包中增加一个插件

该插件会打包到```static/doc```目录中

```xml
<plugin> 
	<artifactId>maven-resources-plugin</artifactId>
	<version>2.7</version>
	<executions>
		<execution>
			<id>copy-resources</id>
			<phase>prepare-package</phase>
			<goals>
				<goal>copy-resources</goal>
			</goals>
			<configuration> 
				<outputDirectory>
					${project.build.outputDirectory}/static/docs
				</outputDirectory>
				<resources>
					<resource>
						<directory>
							${project.build.directory}/generated-docs
						</directory>
					</resource>
				</resources>
			</configuration>
		</execution>
	</executions>
</plugin>
```


>
> 待续
>




 

