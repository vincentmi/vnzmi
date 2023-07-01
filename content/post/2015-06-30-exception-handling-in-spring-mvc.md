---
layout:     post
title:      "Spring MVC 的错误处理"
date:       2015-06-30 17:18:00
author:     "Vincent"
image:  "img/post-bg.jpg"
catalog: true
tags:
    - RD
    - Spring
    - Java
---


Spring MVC 提供多种异常处理方式，但是当我在进行Spring MVC培训时，我发现我的学院经常会感到困惑或者不太适应。

今天我将为你展示多种可能的选项。我们的目标是如果可能的话不在Controller的方法里显式的处理异常。作为横切关注点分别在专用代码里处理更好。


<!--more-->


这里有三个选项：按异常,按控制器或者全局处理

可以在 [http://github.com/paulc4/mvc-exceptions.](http://github.com/paulc4/mvc-exceptions.) 找到关于这个讨论的观点的Demo程序。

注意:演示应用程序已经在2014年10月使用Spring boot 1.1.8,进行修改和更新,希望更容易使用和理解。

## 使用HTTP状态码

通常当处理页面请求时任何未处理的异常将会引起服务器返回一个HTTP 500 的响应。然而，任何你自己编写的异常都可以通过@ResponseStatus注解进行指定（@ResponseStatus 支持HTTP协议中定义的全部状态码）。当一个被注解的异常被控制器方法抛出，并且没有在其他地方被处理过，他将自动产生一个指定status-code的HTTP响应。

例如，这里是一个订单找不到的异常。

```java
    @ResponseStatus(value=HttpStatus.NOT_FOUND, reason="No such Order")  // 404
    public class OrderNotFoundException extends RuntimeException {
        // ...
    }
```  
  这是一个控制器方法中进行使用：

```java  
    @RequestMapping(value="/orders/{id}", method=GET)
    public String showOrder(@PathVariable("id") long id, Model model) {
        Order order = orderRepository.findOrderById(id);
        if (order == null) throw new OrderNotFoundException(id);
        model.addAttribute(order);
        return "orderDetail";
    }
```    
 如果这个URL中包含了一个未知的Order Id，一个和404类似的响应将会被返回。
 
##  使用控制器的异常处理

#### 使用@ExceptionHandler
你可以在任何控制器中添加专门的错误处理方法（增加@EceptionHandler注解）来处理同一个控制器在处理http请求(@RequestMapping注解的方法)时抛出的异常.这些方法需要进行如下处理：

 1. 处理没有被@ResponseStatus注解的异常（指你没有写的预定义异常）
 2. 重定向访客到专门的错误视图
 3. 创建完全定制的错误响应
 
 下面的控制器实现了如上的三点

```java
@Controller
public class ExceptionHandlingController {

  // @RequestHandler methods
  ...
  
  // Exception handling methods
  
  // 转换预定义的异常为HTTP错误代码
  @ResponseStatus(value=HttpStatus.CONFLICT, reason="Data integrity violation")  // 409
  @ExceptionHandler(DataIntegrityViolationException.class)
  public void conflict() {
    // Nothing to do
  }
  
  // 指定一个视图用于显示错误信息r:
  @ExceptionHandler({SQLException.class,DataAccessException.class})
  public String databaseError() {
    // 不做任何事，返回错误代码的视图的名字，通常传递给view-resolver
    //注意这个异常对象不能在view里面使用，他没被加入到model
    // 请查看下面的 "扩展 ExceptionHandlerExceptionResolver" 章节.
    return "databaseError";
  }

  // Total control - setup a model and return the view name yourself. Or consider
  // subclassing ExceptionHandlerExceptionResolver (see below).
  @ExceptionHandler(Exception.class)
  public ModelAndView handleError(HttpServletRequest req, Exception exception) {
    logger.error("Request: " + req.getRequestURL() + " raised " + exception);

    ModelAndView mav = new ModelAndView();
    mav.addObject("exception", exception);
    mav.addObject("url", req.getRequestURL());
    mav.setViewName("error");
    return mav;
  }
}
```

在上面的任何方法中，你可能需要选择进行额外的处理。通常的例子是记录异常的日志。

处理器方法比较灵活你可以传递多种servlet相关的对象，比如 HttpServletRequest,HttpServletResponse ,HttpSession 和Principle

**注意：Model不要作为任何@ExceptionHandler方法的参数。使用上面handleError示例中的方式在方法内使用一个ModelAndView创建一个Model.**


#### 异常和视图 ####

在model里增加异常要非常小心。你的用户不希望在页面中看到java的异常详情和堆栈跟踪。然后将异常的详情以注释的方式放在页面源代码中可以有效的帮助进行技术支持的同事。如果使用JSP你可以输入异常和相应的错误跟踪信息到一个隐藏的div中。
```html
    <h1>Error Page</h1>
    <p>Application has encountered an error. Please contact support on ...</p>
    
    <!--
    Failed URL: ${url}
    Exception:  ${exception.message}
        <c:forEach items="${exception.stackTrace}" var="ste">    ${ste} 
    </c:forEach>
    -->
```
使用Thymeleaf的代码 [support.html](https://github.com/paulc4/mvc-exceptions/blob/master/src/main/resources/templates/support.html)

## 全局错误处理

### 使用@ControllerAdvice 类
一个Advice控制器允许你在整个应用程序中使用完全相同的错误处理技术。而只是在一个单独的控制器中。你可以把它想象成一个驱动拦截器的注解。

使用@ControllerAdvice使任何的类变成一个Advice 控制器，他支持三种类型的方法：
1. 注解为@ExceptionHandler的错误处理方法
2. 模型增强方法（为了增加额外的数据到model中），注解为@ModelAttribute .注意这些属性不能使用到异常处理视图中
3. Binder的初始化(用于配置一些表单处理)，使用@InitBinder注解

我们只考虑@ControllerAdvice方法的错误处理，更多请查看在线手册

你在上面例子中看到的异常处理器都快要定义到controller-advice类中，但是现在他们被用于处理从所有控制器抛出的异常。这是一个简单的例子：
```java
    @ControllerAdvice
    class GlobalControllerExceptionHandler {
        @ResponseStatus(HttpStatus.CONFLICT)  // 409
        @ExceptionHandler(DataIntegrityViolationException.class)
        public void handleConflict() {
            // Nothing to do
        }
    }
``` 
如果你想用一个默认的异常处理器处理任何的异常，会有一点小麻烦。你需要确定被注解过的异常要被框架处理掉。代码如下：

```java
    @ControllerAdvice
    class GlobalDefaultExceptionHandler {
    public static final String DEFAULT_ERROR_VIEW = "error";

    @ExceptionHandler(value = Exception.class)
    public ModelAndView defaultErrorHandler(HttpServletRequest req, Exception e) throws Exception {
        // 如果异常是使用@ResponseStatus进行注解的再抛出他- 比如OrderNotFoundException这个异常        // AnnotationUtils是Spring Framework的一个工具类
        if (AnnotationUtils.findAnnotation(e.getClass(), ResponseStatus.class) != null)
            throw e;

        // 否则设置和发送给用户一个默认的错误视图
         ModelAndView mav = new ModelAndView();
        mav.addObject("exception", e);
        mav.addObject("url", req.getRequestURL());
        mav.setViewName(DEFAULT_ERROR_VIEW);
        return mav;
    }
    }
```    
## 延伸阅读

### HandlerExceptionResolver
任何在DispatcherServlet应用上下文中定义的实现了HandlerExceptionResolver接口的Bean将被用来拦截和处理由MVC系统抛出而没有被控制器处理过的异常。这个接口定义如下：

```java
    public interface HandlerExceptionResolver {
        ModelAndView resolveException(HttpServletRequest request, 
                HttpServletResponse response, Object handler, Exception ex);
    }
```
    
handler  是产生异常的控制器（记住@Controller实例只是Spring  MVC只是的一种hander类型，例如：HttpInvokerExporter和WebFlowExecutor也是一种handler类型）

在幕后，MVC默认创建三个这样的resolver,正是这些resolver实现上面讨论的行为。 

- ExceptionHandlerExceptionResolver 匹配未捕捉的异常去适配@ExceptionHandler注解的方法和任何controller-advice类

- ResponseStatusExceptionResolver 观察被注解为@ResponseStatus未捕捉的异常.(和在第一部分描述的一样)
- DefaultHandlerExceptionResolver 转换标准的Spring异常为HTTP状态码（我上面没有提到是因为这个是Spring MVC内部的行为）

他们是一个链表并且在有序的列表进行处理。（在内部Spring 创建了一个独立的Bean HandlerExceptionResplverComposite 来做这个）

注意，方法的签名为resolveException,不包含Model,这就是为什么@ExceptionHandler方法不能被注入model .

如果愿意你可以自己实现一个HandlerExceptionResolver来设置自己定制的异常处理系统。处理器通常实现Spring的Ordered接口，这样你可以定义处理器的运行顺序。

### SimpleMappingExceptionResolver
Sping一直提供一个简单而方便的HandlerExceptionResolver实现 .你可能已经发现这个类SimpleMappingExceptionResolver已经在你的应用程序中使用了。

他提供以下选项

- 映射异常类名到视图的名字，只是指定类名，不需要包名
- 指定一个默认的后备的错误页面给没有在其他地方处理过的异常
- 记录日志（默认未打开）
- 为模型设置一个 exception属性，这样他就可以再视图里使用了。默认这个属性被命名为exception,设置为null禁用这个功能，注意从@ExceptionHandler注解方法返回的视图不能访问exception但是SimpleMappingExceptionResolver却可以。

这是一个典型的使用XML的配置:


```xml
        <bean id="simpleMappingExceptionResolver"
              class="org.springframework.web.servlet.handler.SimpleMappingExceptionResolver">
            <property name="exceptionMappings">
                <map>
                    <entry key="DatabaseException" value="databaseError"/>
                    <entry key="InvalidCreditCardException" value="creditCardError"/>
                </map>
            </property>
            <!-- See note below on how this interacts with Spring Boot -->
            <property name="defaultErrorView" value="error"/>
            <property name="exceptionAttribute" value="ex"/>
            
            <!-- Name of logger to use to log exceptions. Unset by default, so logging disabled -->
            <property name="warnLogCategory" value="example.MvcLogger"/>
        </bean>


或者使用Java配置

        @Configuration
        @EnableWebMvc   // Optionally setup Spring MVC defaults if you aren't doing so elsewhere
        public class MvcConfiguration extends WebMvcConfigurerAdapter {
            @Bean(name="simpleMappingExceptionResolver")
            public SimpleMappingExceptionResolver createSimpleMappingExceptionResolver() {
                SimpleMappingExceptionResolver r =
                      new SimpleMappingExceptionResolver();

                Properties mappings = new Properties();
                mappings.setProperty("DatabaseException", "databaseError");
                mappings.setProperty("InvalidCreditCardException", "creditCardError");

                r.setExceptionMappings(mappings);  // None by default
                r.setDefaultErrorView("error");    // No default
                r.setExceptionAttribute("ex");     // Default is "exception"
                r.setWarnLogCategory("example.MvcLogger");     // No default
                return r;
            }
            ...
        }
```

defaultErrorView属性特别有用,因为它可以确保任何未捕获的异常产生一个合适的应用程序定义的错误页面。（默认很多应用服务器会显示一个java的错误跟踪信息，这个用户不应该看到的东西）

### 扩展SimpleMappingExceptionResolver 
扩展SimpleMappingExceptionResolver通常为了实现：

- 使用构造函数直接设置属性值，例如允许异常日志和设置日志记录器
- 通过重写buildLogMessage覆盖默认的日志消息。默认的实现一直返回固定的文本 

> Handler execution resulted in exception
 
- 通过重载doResolveException去添加附加信息到错误视图。

例如 ：

```java
    public class MyMappingExceptionResolver extends SimpleMappingExceptionResolver {
        public MyMappingExceptionResolver() {
            // Enable logging by providing the name of the logger to use
            setWarnLogCategory(MyMappingExceptionResolver.class.getName());
        }

        @Override
        public String buildLogMessage(Exception e, HttpServletRequest req) {
            return "MVC exception: " + e.getLocalizedMessage();
        }
        
        @Override
        protected ModelAndView doResolveException(HttpServletRequest request,
                HttpServletResponse response, Object handler, Exception exception) {
            // Call super method to get the ModelAndView
            ModelAndView mav = super.doResolveException(request, response, handler, exception);
            
            // Make the full URL available to the view - note ModelAndView uses addObject()
            // but Model uses addAttribute(). They work the same. 
            mav.addObject("url", request.getRequestURL());
            return mav;
        }
    }
```

这段代码在Demo应用中在[ExampleSimpleMappingExceptionResolver.java](https://github.com/paulc4/mvc-exceptions/blob/master/src/main/java/demo1/web/ExampleSimpleMappingExceptionResolver.java)


### 扩展ExceptionHandlerExceptionResolver
也可以使用同样的方法重载doResolveHandlerMethodException来扩展ExceptionHandlerExceptionResolver.他们有同样的签名(只是名字由Handler变成HandlerMethod)

为了让这个类被使用也要设置一个继承的order属性（例如：在新类的构造函数执行）的值为比MAX_INT小的值。这样这个ExceptionHandlerExceptionResolver对象将在默认对象前面执行。
查看demo代码 [ExampleExceptionHandlerExceptionResolver.java](https://github.com/paulc4/mvc-exceptions/blob/master/src/main/java/demo/example/ExampleExceptionHandlerExceptionResolver.java)

### REST中的错误
RESTful 的GET请求可能也会产生错误。我们已经看到如何返回一个标准的HTTP错误代码。然而如果你想返回这个错误的信息呢？这非常简单。
首先定义一个一个错误类

```java
        public class ErrorInfo {
            public final String url;
            public final String ex;

            public ErrorInfo(String url, Exception ex) {
                this.url = url;
                this.ex = ex.getLocalizedMessage();
            }
        }

现在我们可以从handler返回一个实例到@ResponseBody,像这样

        @ResponseStatus(HttpStatus.BAD_REQUEST)
        @ExceptionHandler(MyBadDataException.class)
        @ResponseBody ErrorInfo handleBadRequest(HttpServletRequest req, Exception ex) {
            return new ErrorInfo(req.getRequestURL(), ex);
        } 
        
```

### 什么时候使用

和往常一样Spring喜欢让你选择。你应该怎么做？这里有一些规则

- 你自己写的异常考虑给他们添加@ResponseStatus.
- 为其他的所有异常在@ControllerAdvice类实现一个@ExceptionHandler方法或则使用一个SimpleMappingExceptionResolver实例。你很可能已经配置了SimpleMappingExceptionResolver到你的应用程序。在这种情况下添加新的异常类可能比实现@ControllerAdvice更容易。
- 为控制器指定异常处理添加@ExceptionHandler方法到你的控制器
- 警告：在同一个应用程序中混合多个选项要很小心。如果一个异常能被超过一个方法处理，你可能不会得到你想要的行为。控制器的@ExceptionHandler方法一直会在任何@ControllerAdvice实例之前被选择。这是未定义的controller-advice处理顺序

### DEMO地址
Git http://mvc-exceptions-v2.cfapps.io/
http://mvc-exceptions-v2.cfapps.io/


## Spring Boot 和错误处理

Spring Boot 允许spring项目使用最小配置进行安装。
Spring Boot当它在classpath中检测到某些关键类和包时会自动创建合理的默认值。
例如如果他发现你正在使用Servlet环境，他会使用最普遍的Spring MVC设置，视图检测和映射处理器等。
如果它发现JSP 以及Thymeleaf，它会设置他们的模板技术。

Spring MVC并没有提供默认的开箱即用的错误页面。最常见的设置一个默认错误处理页面一直是 SimpleMappingExceptionResolver(  实际从 Spring V1开始)。
然而Spring Boot提供一个备用的错误处理页面。

开始时Spring Boot尝试查找/error的映射。根据约定，一个由/error结尾的URL映射到同样名字的error视图。在demo中这个视图映射转到Thymeleaf引擎的error.html 。（如果使用JSP根据你的InternalResourceViewResolver的设定应该映射到error.jsp ）

如果没有到映射到/error的视图。Spring定义他自己的备用错误页面。这个所谓的"Whitelabel Error Page" (一个包含HTTP状态码信息和一些页面详情，例如未捕捉的异常信息)。如果你将error.html改名称 error2.html然后重启，你就会发现这个页面被使用了。

通过定义Java配置名脚defaultErrorView()的@Bean方法，你可以返回你自己的错误视图实例。（查阅Spring Boot的ErrorMvcAutoConfiguration类获取更多细节）

如果你已经使用SimpleMappingExceptionResolver设置了一个默认的错误视图怎么办？简单，确保defaultErrorView定义了与SpringBoot相同的error视图。或者你可以通过设置属性error.whitelabel.enabled 为false来禁用Spring Boot的错误页面。你的容器的偶人错误页将会替代他。
这里是一个在构造函数使用Spring Boot属性的[例子](https://github.com/paulc4/mvc-exceptions/blob/master/src/main/java/demo/main/Main.java)

```java
    Properties props = new Properties();
    props.setProperty("spring.thymeleaf.cache", "false");
    props.setProperty("error.path", "/error");
    props.setProperty("error.whitelabel.enabled", "true");
    props.setProperty("org.springframework.web", "DEBUG");
    SpringApplicationBuilder application = new SpringApplicationBuilder();
    application.sources(Main.class);
    ...
    application.properties(props);
```

留意在demo里，SimpleMappingExceptionResolver的defaultErrorView属性故意设置
为defaultErrorPage而不是error.所以你可以看到什么时候是handler生成的错误页面，什么时候
是Sping Boot在相应。正常情况两者都应该被设置为error

还在我演示应用程序展示了如何创建一个对技术支持友好的错误页面，
将错误跟踪信息隐藏在HTML源代码注释中。理想情况下技术支持应该从日志应中获取这些信息,但是生活并不是一直理想的。
无论如何,hadleError创建自己的ModelAndView来提供额外的信息给错误页面。

请参考如下代码  
ExceptionHandlingController.handleError()  [github](http://github.com/paulc4/mvc-exceptions/blob/master/src/main/java/demo1/web/ExceptionHandlingController.java)
GlobalControllerExceptionHandler.handleError()  [github](https://github.com/paulc4/mvc-exceptions/blob/master/src/main/java/demo2/web/GlobalExceptionHandlingControllerAdvice.java)



原文:[Paul Chapman](https://spring.io/blog/2013/11/01/exception-handling-in-spring-mvc)  
翻译:[Vincent Mi](http://vnzmi.com)




