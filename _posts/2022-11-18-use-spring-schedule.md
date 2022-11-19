---
layout:     post
title:      "深入使用Spring计划任务框架"
date:       "2022-11-18 11:11:00"
author:     "Vincent"
header-img:  "img/leaf.jpg"
catalog: true
tags:
    - Spring
    - SpringBoot
    - Java
    - Schedule
---

##  任务执行和计划

Spring框架提供```TaskExecutor```和```TaskSchedule```接口对异步任务和计划任务进行抽象。并支持很多框架的特性，比如线程池和委派等。这些接口在不同的运行环境背后通过不同的实现来进行支持。

Spring支持使用```Timer```和Quartz Scheduler ( https://www.quartz-scheduler.org/)进行调度。

## TaskExecutor 接口

```TaskExecutor```和```java.util.concurrent.Executor```接口一样， 用于对需要线程池的地方进行抽象，如果你的组件需要一些线程池的支持，可以使用该接口。

Spring提供了一些预置的```TaskExecutor```的实现。

- ```SyncTaskExecutor``` 同步执行器，任务会在当前线程进行执行，主要用于不需要多线程的场景或者测试的时候。
- ```SimpleAsyncTaskExecutor``` 简单的异步执行器。不进行线程复用。每次调用都会启动一个新线程。他支持并发限制，如果调用超出了限制，会阻塞到有插槽释放才能被调用。
- ```ConcurrentTaskExecutor``` 此实现是 ```java.util.concurrent.Executor```实例到适配器。作为```ThreadPoolTaskExecutor```用于暴露```Executor```配置选项的的实现。比较少能用到这个实现，当然如果```ThreadPoolTaskExecutor```不够灵活无法满足你的需求，你可以选择使用这个实现。
- ```ThreadPoolTaskExecutor```  这个实现是通常会使用的哟个实现。它暴露了用于配置 ```java.util.concurrent.ThreadPoolExecutor``` 的 bean 属性并将其包装在``` TaskExecutor``` 中。如果需要包装成```java.util.concurrent.Executor```你可以选择上一个实现类。
- ```DefaultManagedTaskExecutor```：此实现用于用于  兼容JSR-236运行时环境（例如 Jakarta EE 应用程序服务器）通过 JNDI 获得的 ```ManagedExecutorService```。

#### 使用 TaskExecutor
像简单的Bean一样使用 ```TaskExecutor```即可。手动使用如下

>
>  如下代码
>  Test服务构建完成后就提交了50个任务，分别打印任务的编号
>

```java
@Slf4j
@Service
public class Test {

    @PostConstruct
    private void test(){
        SimpleAsyncTaskExecutor simpleAsyncTaskExecutor = new SimpleAsyncTaskExecutor();
        simpleAsyncTaskExecutor.setThreadGroupName("test1");
        simpleAsyncTaskExecutor.setDaemon(true);
        simpleAsyncTaskExecutor.setConcurrencyLimit(10);
        simpleAsyncTaskExecutor.setThreadPriority(1);
        for(int i =0;i<50;i++) {
            int finalI = i;
            simpleAsyncTaskExecutor.execute(()->{
                log.info("{}","task-"+ finalI);
                try {
                    Thread.sleep(5000L);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });
        }
    }
}
```


## TaskScheduler 接口

```TaskScheduler```在 ```TaskExecutor```都基础上定义了任务在未来的某个时间点的执行。定义如下：

```java
public interface TaskScheduler {
    @Nullable
    ScheduledFuture<?> schedule(Runnable var1, Trigger var2);
    
    // 在指定时间之后执行一次
    default ScheduledFuture<?> schedule(Runnable task, Instant startTime) {
        return this.schedule(task, Date.from(startTime));
    }
    
    // 在指定时间之后执行一次
    ScheduledFuture<?> schedule(Runnable var1, Date var2);

    default ScheduledFuture<?> scheduleAtFixedRate(Runnable task, Instant startTime, Duration period) {
        return this.scheduleAtFixedRate(task, Date.from(startTime), period.toMillis());
    }

    ScheduledFuture<?> scheduleAtFixedRate(Runnable var1, Date var2, long var3);

    default ScheduledFuture<?> scheduleAtFixedRate(Runnable task, Duration period) {
        return this.scheduleAtFixedRate(task, period.toMillis());
    }

    ScheduledFuture<?> scheduleAtFixedRate(Runnable var1, long var2);

    default ScheduledFuture<?> scheduleWithFixedDelay(Runnable task, Instant startTime, Duration delay) {
        return this.scheduleWithFixedDelay(task, Date.from(startTime), delay.toMillis());
    }

    ScheduledFuture<?> scheduleWithFixedDelay(Runnable var1, Date var2, long var3);

    default ScheduledFuture<?> scheduleWithFixedDelay(Runnable task, Duration delay) {
        return this.scheduleWithFixedDelay(task, delay.toMillis());
    }

    ScheduledFuture<?> scheduleWithFixedDelay(Runnable var1, long var2);
}
```

```schedule(Runnable task, Instant startTime)``` 接口用于任务在指定时间之后执行。

```scheduleAtFixedRate(Runnable task, Duration period)``` 在指定的时间间隔后执行

```scheduleAtFixedRate(Runnable task, Duration period)``` 在指定的时间间隔后执行

```scheduleWithFixedDelay(Runnable var1, Date var2, long var3)``` 在时间点之后间隔的时间执行

```schedule(Runnable var1, Trigger var2)``` 使用```Trigger```来触发任务的执行，通过更加复杂的设置来执行任务。

#### Trigger接口

Trigger接口通过指定一个时间来计算出下一次执行的时间。接口定义如下：

```java
public interface Trigger {
    Date nextExecutionTime(TriggerContext triggerContext);
}
```

```TriggerContext```接口提供用于计算的数据

```java
public interface TriggerContext {
    Date lastScheduledExecutionTime();
    Date lastActualExecutionTime();
    Date lastCompletionTime();
}
```

Spring  提供了两个```Trigger``` 的实现。```CronTrigger```,允许使用定时任务表达式来触发任务的执行: 例如:工作日上午9点到下午5点每小时到15分执行任务.

```java
scheduler.schedule(task,new CronTrigger("0 15 9-17 * * MON-FRI"));
```
另一个实现 ```PeriodicTrigger``` ,主要用于实现 ```scheduleWithFixedDelay```和```scheduleAtFixedRate```功能,为了保持组件的接口统一.日常使用建议还是直接调用```Schedule```的方法.


####  TaskScheduler的实现

与Spring的```TaskExecutor```抽象一样，```TaskScheduler``` 主要为了将开发和部署进行分离。当部署到应用程序服务器环境时，因为应用程序本身不应该直接创建线程。对于这样的场景，Spring提供了一个```TimerManagerTaskScheduler```，它委托给WebLogic或WebSphere上的CommonJ ```TimerManager```，以及一个更新的```DefaultManagedTaskScheduler```，在Jakarta EE环境中委托给JSR-236 ```ManagedScheduledExecutorService```。两者通常都配置有JNDI查找。

当不需要外部线程管理时，一个更简单的替代方案就是在应用程序中设置本地```ScheduledExecutorService```，它可以通过Spring的```ConcurrentTaskScheduler```进行调整。为了方便起见，Spring还提供了```ThreadPoolTaskScheduler```，它在内部委托给```ScheduledExecutorService```，以提供与```ThreadPoolTaskExecutor```类似的通用bean样式配置。这些变体更适合用于Tomcat和Jetty环境中。

## 注解支持

你需要在应用中开启计划任务和异步的支持,使用 ```@EnableScheduling``` 和 ```@EnableAsync```开启后,你可以很方便的使用``` @Scheduled``` 和 ```@Async ``` 来使用他.

>
> Spring通常在 Application.class 里使用这些注解.
>

```java
@Configuration
@EnableAsync
@EnableScheduling
public class AppConfig {
}
```

#### @Schedule 注解使用


每5秒执行一次

```java
@Scheduled(fixedDelay = 5000)
public void doSomething() {
    // something that should run periodically
}
```

上一次执行完5秒后再执行

initialDelay = 1000 设置延迟1秒再启动任务

```java
@Scheduled(initialDelay = 1000, fixedDelay = 5000)
public void doSomething() {
    // something that should run periodically
}
```

使用CRON表达式

```java
@Scheduled(cron="*/5 * * * * MON-FRI")
public void doSomething() {
    // something that should run on weekdays only
}
```

> 使用 ```zone``` 参数可以指定时区.
> 

#### @Async 注解使用

增加  @Async 注解会使对方法的调用被提交到一个 ```TaskExecutor```,异步进行执行.

```java
@Async
void doSomething() {
    // this will be run asynchronously
}
```

和 ```@Schedule```不同,这些方法可以接受参数,因为他们是被正常的方式进行调用.而计划任务由容器进行管理.

```java
@Async
void doSomething(String s) {
    // this will be run asynchronously
}
```

方法也可以返回一个 ```Future``` 类型的返回值.使用 ```Future.get```来获取异步的返回值.

```java
@Async
Future<String> returnSomething(int i) {
    // this will be run asynchronously
}
```
返回值除了可以定义为 ```java.util.concurrent.Future``` 也可以使用 ```org.springframework.util.concurrent.ListenableFuture```,以及 ```java.util.concurrent.CompletableFuture```
来更方便的使用.

注意你不能在Bean的生命周期回调中使用该注解 ,比如 ```@PostConstruct```.你可以使用一个专门的初始化Bean来达到这个效果.

```java 
public class SampleBeanImpl implements SampleBean {

    @Async
    void doSomething() {
        // ...
    }

}

public class SampleBeanInitializer {

    private final SampleBean bean;

    public SampleBeanInitializer(SampleBean bean) {
        this.bean = bean;
    }

    @PostConstruct
    public void initialize() {
        bean.doSomething();
    }

}

```

```@Async```也可以指定 要使用的```Executor```的名称,来使用其他的执行器.

```java
@Async("otherExecutor")
void doSomething(String s) {
    // this will be run asynchronously by "otherExecutor"
}
```

## Cron 表达式

```txt
 ┌───────────── second (0-59)
 │ ┌───────────── minute (0 - 59)
 │ │ ┌───────────── hour (0 - 23)
 │ │ │ ┌───────────── day of the month (1 - 31)
 │ │ │ │ ┌───────────── month (1 - 12) (or JAN-DEC)
 │ │ │ │ │ ┌───────────── day of the week (0 - 7)
 │ │ │ │ │ │          (0 or 7 is Sunday, or MON-SUN)
 │ │ │ │ │ │ 
 * * * * * * 

```


#### 特殊字符

| 字符 | 描述 | 示例 |
| --- | --- | --- |
| * | 用于表示给定的所有值 | | 
| ? | 用于表示未指定的任何值,用于dayOfMonth字段和dayOfWeek字段 | | 
| - | 用于表示范围 | 5-7  包含 5,6,7 | 
| , | 用于分割多个值 | 5,7  包含 5,7 | 
| / | 用于表示间隔 | 0 */3  * * * *  每3分钟执行一次 | 
| L | Last用于表示最后,只能用于dayOfMonth和dayOfWeek字段 | 5L在dayOfWeek表示每月的最后一个周五 | 
| W | Week用于表示有效工作日,只能用于dayOfMonth和dayOfWeek字段 |系统将在离指定日期的最近的有效工作日触发事件  | 
















