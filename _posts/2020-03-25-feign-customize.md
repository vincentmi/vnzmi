---
layout:     post
title:      "Feign自定义配置爱"
date:       "2020-03-25 23:31:00"
author:     "Vincent"
header-img:  "img/home-bg-highway.jpg"
catalog: true
tags:
    - Java
    - OkHttp
    - SSL
---


## 背景

微服务重构,使用Spring全家桶.JSON数据传输为了兼容接口规范对Feign进行了定制

## 启用Feign

 加入Feign的Spring starter依赖
 
```xml
 <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

Applicaiton中加上注解

```java
@SpringBootApplication
@EnableFeignClients
public class Application {

    public static void main(String[] args) {

        SpringApplication.run(Application.class);

    }

}
```

##   定义一个和使用客户端

```java
package com.tourscool.passport;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;

@FeignClient(name="authorize" ,url="http://authorize.dev.philo.in/api/v1/",configuration = FeignConfiguration.class)
public interface AuthorizeClient {

    @RequestMapping(value = "/auth/verify-get", method = RequestMethod.GET)
    PermInfo verifyAndGet(@RequestParam  String token, @RequestParam  long applicationId);

}
```

在 ```AuthorizeClient``` 这个接口中我们定义了一个```verifyAndGet```的方法,用于进行TOKEN的验证.

```@FeignClient(name="authorize" ,url="http://authorize.dev.philo.in/api/v1/",configuration = FeignConfiguration.class)```
这个注解启用 Feign客户端. ```name```字段在启用了服务发现之后会从服务发现中获取到你所要调用的
服务的真实地址.调试时可以设置```url```来指定你的地址.

```configuration``` 则用于指定该客户端在发送HTTP 请求的一些行为.通过这个class我们可以对Feign进行深度的定制.

```java
@RestController
public class Endpoint {

    @Value("${application.name:passport}")
    private String name;

    @Autowired
    private AuthorizeClient client;

    @GetMapping("/")
    public HashMap<String,Object> info(String token)
    {
        PermInfo info = client.verifyAndGet(token,1);
    }
```

定义好接口之后我们可以直接进行使用.Feign会帮我们创建实例.

## 定制

Feign 的定制通过指定configuration 类来实现.非常方便.也可以使用spring扫描配置来应用到全局.

旧的规范我们定义了接口的结构如下,

```json
{
  "code": 0,
  "msg": "success",
  "data": {
      "name" : "vincent",
      "salary" : 800
  }
}
```

异常情况

```json
{
  "code": 600403,
  "msg": "Access Deny",
  "data": null
  }
```

我们希望在Feign使用中,发现异常情况直接抛出异常,而如果执行正常则需要直接返回实际的数据结构.

因此我们需要自己实现一个Feign的```Decoder```用于将Feign返回的内容转换成对象.
代码如下:

```java
旧的规范我们定义了接口的结构如下,

```json
package com.tourscool.passport;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import com.vnzmi.commons.exception.BusinessException;

import feign.Logger;
import feign.Types;
import feign.Util;
import feign.codec.Decoder;
import org.springframework.context.annotation.Bean;

import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;

public class FeignConfiguration {
    @Bean
    Logger.Level feignLoggerLevel() {
        return Logger.Level.FULL;
    }

    @Bean
    public Decoder decoder(){
        return (response, type) -> {
            String bodyText = Util.toString(response.body().asReader(StandardCharsets.UTF_8));
            ObjectMapper mapper = new ObjectMapper();
            JsonNode root = mapper.readTree(bodyText);
            JsonNode codeNode = root.get("code");
            JsonNode msgNode = root.get("msg");
            if(codeNode == null || codeNode == null)
            {
                throw new BusinessException(400,"unsupported rest format");
            }
            int code = codeNode.asInt();
            String message = msgNode.asText();

            if(code  != 0 )
            {
                throw new BusinessException(500,"rpc error ["+message+"]");
            }

            JsonNode dataNode = root.get("data");
            return mapper.treeToValue(dataNode, Types.getRawType(type));
        };
    }
}
```

另外 Feign 写的 '''Types.getRawType'''还挺好用 ;)

```java
 public static Class<?> getRawType(Type type) {
        if (type instanceof Class) {
            return (Class)type;
        } else if (type instanceof ParameterizedType) {
            ParameterizedType parameterizedType = (ParameterizedType)type;
            Type rawType = parameterizedType.getRawType();
            if (!(rawType instanceof Class)) {
                throw new IllegalArgumentException();
            } else {
                return (Class)rawType;
            }
        } else if (type instanceof GenericArrayType) {
            Type componentType = ((GenericArrayType)type).getGenericComponentType();
            return Array.newInstance(getRawType(componentType), 0).getClass();
        } else if (type instanceof TypeVariable) {
            return Object.class;
        } else if (type instanceof WildcardType) {
            return getRawType(((WildcardType)type).getUpperBounds()[0]);
        } else {
            String className = type == null ? "null" : type.getClass().getName();
            throw new IllegalArgumentException("Expected a Class, ParameterizedType, or GenericArrayType, but <" + type + "> is of type " + className);
        }
    }
```







 

