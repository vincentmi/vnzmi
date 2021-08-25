---
layout:     post
title:      "制作自定义的Spring Starter"
date:       "2021-04-05 10:53:00"
author:     "Vincent"
header-img:  "img/bullseye-gradient_blue.svg"
catalog: true
tags:
    - Spring
    - Spring Boot
    - Java
---

>
> 国内很多文章讲的不详细
>  参考: https://www.baeldung.com/spring-boot-custom-starter
>


## Spring Boot 自动配置原理

Spring Boot启动时会查找```classpath```中是否存在一个 ```spring.factories```的文件.这个文件保存在```META-INF```文件夹. [spring-boot-autoconfigure](https://github.com/spring-projects/spring-boot/blob/master/spring-boot-project/spring-boot-autoconfigure/src/main/resources/META-INF/spring.factories) 项目中该文件代码如下.

```conf

org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
org.springframework.boot.autoconfigure.amqp.RabbitAutoConfiguration,\
org.springframework.boot.autoconfigure.cassandra.CassandraAutoConfiguration,\
org.springframework.boot.autoconfigure.mongo.MongoAutoConfiguration,\
org.springframework.boot.autoconfigure.orm.jpa.HibernateJpaAutoConfiguration

```
这个文件配置了Spring Boot将尝试运行的不同配置类.因此上面的代码Spring 或运行 RabbitMQ,Cassandra,Mongo和HibernateJPA的配置类.

这些类实际是否会被执行取决于某些依赖的类是否出现在类加载路径中.如下代码:

```java
@Configuration
@ConditionalOnClass(MongoClient.class)
@EnableConfigurationProperties(MongoProperties.class)
@ConditionalOnMissingBean(type = "org.springframework.data.mongodb.MongoDbFactory")
public class MongoAutoConfiguration {
    // configuration code
}
```
上面这个```MongoAutoConfiguration```当```MongoClient.class```存在于类路径中时,则会加载Mongo相关的配置工作.

```@ConditionalOnClass(MongoClient.class)``` 判断类是否出现在路径中.


## 为```application.properties```文件定制配置项

Spring Boot通过一些预定于的默认值来初始化bean,为了覆盖这些默认配置,我们通过```application.properties``` 中的一些特定的名字来定义他.这些配置会被容器自动加载.

来看看他的工作原理. 在上面的代码中 ```@EnableConfigurationProperties(MongoProperties.class)
``` 声明了使用```MongoProperties.class```作为自定义配置的容器. ```MongoProperties.class```代码如下 : 

```java
@ConfigurationProperties(prefix = "spring.data.mongodb")
public class MongoProperties {
    private String host;
    // other fields with standard getters and setters
}
```
```@ConfigurationProperties``` 声明了配置项的前缀.如果我们要设置```host```属性需要设置

```properties
spring.data.mongodb.host= localhost
```
其他属性类似.


## 创建自己的starter

基于上面的原理,要编写我们自己的starter需要完成以下组件:

- 一个为我们的库进行自动配置的类.他拥有一个自定义配置
- 一个```pom```引入我们的库和自动配置项目的依赖

在示例中我们会创建一个简单的问候库,这个库会通过配置来在一天的某个时候输出问候消息.我们也会创建一个简单的spring 应用使用这个starter模块来进行自动配置.

#### 自动配置模块

自动配置模块我们命名为 ```greeter-spring-boot-autoconfig```.这个模块有两个主要类,```GreeterProperties```允许通过```application.properties```文件进行自定义配置.```GreeterAutoConfiguartion```会为问候库创建一个bean.


```java
//GreeterProperties.java
@ConfigurationProperties(prefix = "baeldung.greeter")
public class GreeterProperties {

    private String userName;
    private String morningMessage;
    private String afternoonMessage;
    private String eveningMessage;
    private String nightMessage;

    // standard getters and setters
}
```

```java 
//GreeterAutoConfiguartion.java
@Configuration
@ConditionalOnClass(Greeter.class)
@EnableConfigurationProperties(GreeterProperties.class)
public class GreeterAutoConfiguration {

    @Autowired
    private GreeterProperties greeterProperties;

    @Bean
    @ConditionalOnMissingBean
    public GreetingConfig greeterConfig() {

        String userName = greeterProperties.getUserName() == null
          ? System.getProperty("user.name") 
          : greeterProperties.getUserName();
        
        // ..

        GreetingConfig greetingConfig = new GreetingConfig();
        greetingConfig.put(USER_NAME, userName);
        // ...
        return greetingConfig;
    }

    @Bean
    @ConditionalOnMissingBean
    public Greeter greeter(GreetingConfig greetingConfig) {
        return new Greeter(greetingConfig);
    }
}
```

我们也需要在  ```src/main/resources/META-INF``` 目录创建一个```spring.factories```文件,内容如下:

```conf
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
  com.baeldung.greeter.autoconfigure.GreeterAutoConfiguration
```

应用程序运行时,如果```Greeter```出现在类路径中,```GreeterAutoConfiguration```类就会被执行.如果成功执行,他将通过```GreeterProperties```读取配置文件,创建```GreeterConfig```和 ```Greeter``` bean 填充到Spring的上下文中.

注解```@ConditionalOnMissingBean ```确保只有当这个bean没有被创建才会进行创建.这样我们就允许用户通过定义自己的bean 来覆盖掉自动配置的bean.


#### 创建```pom.xml```

现在我们来创建starter 的```pom``` 文件,这个文件引入了自动配置和greeter库的依赖.

根据Spring Boot 的命名规则 statrter应该命名为 ```xxxx-spring-boot-starter```这种格式,我们的starter命名为 ```greeter-spring-boot-starter```

```xml
<project ...>
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.baeldung</groupId>
    <artifactId>greeter-spring-boot-starter</artifactId>
    <version>0.0.1-SNAPSHOT</version>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <greeter.version>0.0.1-SNAPSHOT</greeter.version>
        <spring-boot.version>2.2.6.RELEASE</spring-boot.version>
    </properties>

    <dependencies>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
            <version>${spring-boot.version}</version>
        </dependency>

        <dependency>
            <groupId>com.baeldung</groupId>
            <artifactId>greeter-spring-boot-autoconfigure</artifactId>
            <version>${project.version}</version>
        </dependency>

        <dependency>
            <groupId>com.baeldung</groupId>
            <artifactId>greeter</artifactId>
            <version>${greeter.version}</version>
        </dependency>

    </dependencies>

</project>
```

##  使用starter

 要使用我们的starter 只需要在 项目的```pom.xml```加上

 ```xml

 <dependency>
    <groupId>com.baeldung</groupId>
    <artifactId>greeter-spring-boot-starter</artifactId>
    <version>${greeter-starter.version}</version>
</dependency>
 ```

 Spring Boot将会自动将一切配置好,并且我们会有一个已经注入到容器的```Greeter```的bean.

 如果要修改一下默认配置,只需要在项目的 ```application.properties```中增加一些配置:

 ```
 baeldung.greeter.userName=Baeldung
baeldung.greeter.afternoonMessage=Woha Afternoon
 ```

 最后我们再应用程序当中直接使用 ```Greeter``` bean即可 

 ```java
 @SpringBootApplication
public class GreeterSampleApplication implements CommandLineRunner {

    @Autowired
    private Greeter greeter;

    public static void main(String[] args) {
        SpringApplication.run(GreeterSampleApplication.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        String message = greeter.greet();
        System.out.println(message);
        }
}
 ```


完整代码 
https://github.com/eugenp/tutorials/tree/master/spring-boot-modules/spring-boot-custom-starter

## 增加配置项提示

Spring自带的starter在IDEA中修改配置时会展示一个提示.包含默认值和简单说明.

![spring-hint](/img/in-post/spring-hint.png)

IDEA会解析包中的```META-INFO/spring-configuration-metadata.json``` 文件来显示这些内容.因此我们自己的Starter要实现这个功能.只需要增加这个文件就可以了.

```json
{

  "properties": [
    {
      "name": "baeldung.greeter.user-name",
      "type": "java.lang.String",
      "description":"名字",
      "sourceType": "xxxx.xxx.GreeterProperties"
    },
 }
```

