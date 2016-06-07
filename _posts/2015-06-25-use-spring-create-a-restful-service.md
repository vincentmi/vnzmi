---
layout:     post
title:      "用Spring创建RESTful 服务"
date:       2015-06-25 13:52:00
author:     "Vincent"
header-img:  "img/post-bg.jpg"
catalog: true
tags:
    - RD
    - Spring
    - Java
---

这个指南将引导你使用创建一个"hello world"[ RESTFul 服务](http://spring.io/understanding/REST)。


<!--more-->


## 我们将创建

我们创建一个服务 ,接收 HTTP GET 请求在:

    http://localhost:8080/greeting

返回一个Json格式的祝福语 :

    {"id":1,"content":"Hello, World!"}

你可以自定义一个请求，通过在QueryString添加一个name参数:

    http://localhost:8080/greeting?name=User

Name参数将覆盖掉默认的'World'并反映到服务的返回值中：

    {"id":1,"content":"Hello, User!"}

## 准备工作

- 你大约需要15分钟
- 你熟悉的文本编辑器或IDE
- JDK 1.7或以上
- Gradle 2.3+或者Maven 3.0+
- 你也可以用STS工具玩这个(没玩过 搞不懂)

## 如何完成这个指南

同大部分spring的入门指南一样。你可以一步步来进行或者跳过一些基本的你已经熟悉的步凑，两种方式你都可以完成工作代码。

已经完成的代码可以从这里拿到

    git clone https://github.com/spring-guides/gs-rest-service.git
    cd into gs-rest-service/initial

## 使用Gradle构建
首先你需要设置基本的构建脚本，你可以使用任何你喜欢的构建系统来构建Spring应用程序，这里提供使用 Gradle和 Maven进行构建的脚本。[参考文档：使用gradle构建Java项目](http://spring.io/guides/gs/gradle)

### 创建目录结构
项目的目录结构如下 

    |---src
            |---main
                   |---java
                          |---hello

### 创建Gradle构建文件
创建build.gradle内容如下，[下载](https://github.com/spring-guides/gs-rest-service/blob/master/initial/build.gradle)


    buildscript {
        repositories {
            mavenCentral()
        }
        dependencies {
            classpath("org.springframework.boot:spring-boot-gradle-plugin:1.2.3.RELEASE")
        }
    }

    apply plugin: 'java'
    apply plugin: 'eclipse'
    apply plugin: 'idea'
    apply plugin: 'spring-boot'

    jar {
        baseName = 'gs-rest-service'
        version =  '0.1.0'
    }

    repositories {
        mavenCentral()
    }

    sourceCompatibility = 1.7
    targetCompatibility = 1.7

    dependencies {
        compile("org.springframework.boot:spring-boot-starter-web")
        testCompile("junit:junit")
    }

    task wrapper(type: Wrapper) {
        gradleVersion = '2.3'
    }


Spring Boot gradle plugin 提供许多便利特性:

- 他手机所有的Classpath里的Jar文件，构建一个独立可运行的I"über-jar", 这样你可以更方便的运行和传播你的服务.
- 他回查找public static void main()这样的入口方法标记为可执行Class .
- 内建一个依赖处理器，It provides a built-in dependency resolver that sets the version number to match Spring Boot dependencies. You can override any version you wish, but it will default to Boot’s chosen set of versions.


## 使用Maven构建
废话同上, [参考文档：使用Maven构建Java项目](http://spring.io/guides/gs/maven).

###创建目录结构
项目的目录结构如下 

    |---src
            |---main
                   |---java
                          |---hello
                          
                          
pom.xml



    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <groupId>org.springframework</groupId>
        <artifactId>gs-rest-service</artifactId>
        <version>0.1.0</version>

        <parent>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-parent</artifactId>
            <version>1.2.3.RELEASE</version>
        </parent>

        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-web</artifactId>
            </dependency>
        </dependencies>

        <properties>
            <java.version>1.7</java.version>
        </properties>


        <build>
            <plugins>
                <plugin>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-maven-plugin</artifactId>
                </plugin>
            </plugins>
        </build>

        <repositories>
            <repository>
                <id>spring-releases</id>
                <url>https://repo.spring.io/libs-release</url>
            </repository>
        </repositories>
        <pluginRepositories>
            <pluginRepository>
                <id>spring-releases</id>
                <url>https://repo.spring.io/libs-release</url>
            </pluginRepository>
        </pluginRepositories>
    </project>  
    
基本和gradle一致

## 创建资源表示类
现在你设置好了构建系统，你可以创建你自己的web service 了。

我们从思考这个服务的交互开始。

这个服务会处理 GET请求 /greeting .  name参数可选，GET请求会返回一个200 OK，返回一个JSON到响应包的body处展示一个问候。返回的结果类似下面
```
    {
        "id": 1,
        "content": "Hello, World!"
    }
``` 
    
这个 id 字段是一个问候的唯一标识。content字段是一个文本的问候内容。

为了表示这个问候的数据模型，你出阿哥就一个资源表示类。提供一个POJO(简单实体类)对象和一些栏位。

```src/main/java/hello/Greeting.java```  


    package hello;

    public class Greeting {

        private final long id;
        private final String content;

        public Greeting(long id, String content) {
            this.id = id;
            this.content = content;
        }

        public long getId() {
            return id;
        }

        public String getContent() {
            return content;
        }
    }


 `正如你下面看到的，Spring使用了 Jackson JSON library 自动将问候对象转化为JSON`

## 创建资源控制器
在Spring的方式来构建RESTful Web服务，HTTP请求由一个控制器处理。这些组件很容易的使用@RestController注解进行标识，并在下面的GreetingController控制器下面通过 /greeting 返回一个Greeting类的实例来处理GET：
```src/main/java/hello/GreetingController.java``` 

    package hello;
    
    import java.util.concurrent.atomic.AtomicLong;
    import org.springframework.web.bind.annotation.RequestMapping;
    import org.springframework.web.bind.annotation.RequestParam;
    import org.springframework.web.bind.annotation.RestController;
    
    @RestController
    public class GreetingController {
    
        private static final String template = "Hello, %s!";
        private final AtomicLong counter = new AtomicLong();
    
        @RequestMapping("/greeting")
        public Greeting greeting(@RequestParam(value="name", defaultValue="World") String name) {
            return new Greeting(counter.incrementAndGet(),
                                String.format(template, name));
        }
    }

这个控制器很简单也很简洁。但是内部发生了什么让我们一步步来分析。

这个 @RequestMapping注解 确保到 /greeting 的HTTP请求被映射到了 greeting() 方法.


> 上面的例子没有限定请求的方式GET  PUT, POST,等等。  
> 因为   @RequestMapping默认映射所有的 HTTP 操作 .   
> 使用    @RequestMapping(method=GET)去限定映射.    
> 

@RequestParam 注解绑定queryString的参数name到  greeting() 方法. 这个参数不是必须的如果参数未出现则使用默认值 "World" .

这个方法体的实现是创建和返回一个新的Greeting对象，对象的id设置为下一个couter的值，根据给定的模板格式化问候语.

一个传统的MVC控制器和上面的RESTful Web服务控制器之间的主要区别是，创建HTTP响应体的方式。不是依靠一个视图技术进行Greeting数据的服务器端渲染HTML，这RESTful Web服务控制器，只需填充并返回一个问候的对象。对象的数据将被直接以JSON写入HTTP响应中。

这些代码使用 Spring 4中的新注解@RestController, 来标记一个控制器每个方法返回一个域对象来代替视图. 他是 @Controller 和 @ResponseBody 的简写。

这个Greeting对象必须转化为 JSON. 感谢Spring提供的HTTP message 转换支持, 你不需要手动进行转换. spring自动载入MappingJackson2HttpMessageConverter 对Greeting 实例转换成JSON.

## 让应用程序执行起来

虽然可以将这个服务按照传统的方式打包成一个WAR文件以便部署到外部的应用容器中，我下面使用更简单的方式，将服务打包成一个独立的应用程序.你的包将所有内容打包成一个可执行的JAR文件，使用古老的 Java main() 方法进行启动. 这样你可以使用Spring支持的嵌入的tomcat servlet容器以HTTP runtime执行而不用部署到外部实例中.（就是他把tomcat也包进来了）
`src/main/java/hello/Application.java`

    package hello;
    
    import org.springframework.boot.SpringApplication;
    import org.springframework.boot.autoconfigure.SpringBootApplication;
    
    @SpringBootApplication
    public class Application {
    
        public static void main(String[] args) {
            SpringApplication.run(Application.class, args);
        }
    }

@SpringBootApplication 是一个快捷的注解，它会添加如下的注解:

@Configuration 标记这个类为一个Bean的源用于应用上下文。tags the class as a source of bean definitions for the application context.
@EnableAutoConfiguration 告诉Spring boot 开始添加添加基于Classpath的Beans. Spring Boot to start adding beans based on classpath settings, other beans, and various property settings.
Normally you would add @EnableWebMvc for a Spring MVC app, but Spring Boot adds it automatically when it sees spring-webmvc on the classpath. This flags the application as a web application and activates key behaviors such as setting up a DispatcherServlet.
@ComponentScan tells Spring to look for other components, configurations, and services in the the hello package, allowing it to find the HelloController.

