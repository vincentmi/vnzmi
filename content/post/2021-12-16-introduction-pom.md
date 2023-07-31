---
layout:     post
title:      "Maven的POM文件"
date:       "2021-12-16 17:36:00"
author:     "Vincent"
image:  "img/post-bg-java.png"
catalog: true
tags:
    - Maven
    - Java
    - pom
---

## 根POM

```pom.xml```文件包含了项目的信息和配置细节,指导Maven 如何进行构建.他通过继承根 pom来载入Maven的默认配置, 在这个文件中包含了大部分项目会使用到的默认值. 比如对```target```目录的定义,源文件```src/main/java```以及测试代码源文件```src/test/java```的路径定义.Maven执行时在当前目录查找```pom.xml```文件,读取POM文件获取到需要的信息来执行指定的目标.  如果没有明确的指定,所有POM属性将继承自根POM文件.

## 最小配置

POM文件至少需要配置以下五个属性

- ```project``` 根节点
- ```modelVersion``` 该配置文件的版本,设置为```4.0.4```
- ```groupId``` 项目所属组的ID,为了避免冲突通常我们使用域名反写来设置
- ```artifactId``` 制品ID,设置编译生产的内容的ID
- ```version``` 制品在该组下的版本号

#### 示例:

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.vnzmi.test</groupId>
  <artifactId>maven-test</artifactId>
  <version>1</version>
</project>
```

通过 ```groupId```,```artifactId```,```version```,我们可以得到项目的全限定名称,格式 ```<groupId>:<artifactId>:<version>```, 上面例子的名字就是 ```com.vnzmi.test:maven-test:1```,Maven就是通过这个名字到库中进行搜索和加载的. 每个项目都会有一个打包类型,通过```packaging```属性来设置.如果你不设置则会使用默认值 ```jar```,Maven会帮你把编译的内容打包成JAR文件.

刚才的示例中我们没有配置 ```repositories``` 属性,这样我们在构建时如果有需要下载的依赖,Maven会使用根POM里配置的属性,从Maven中央库 ```https://repo.maven.apache.org/maven2```来下载我们的依赖.

## 项目继承

项目会从上级POM合并以下几种元素

- ```dependencies``` 项目的依赖
- ```developer```和```contributors``` 开发者和贡献者
- ```pluginRepositories ```  和```reports```元素
- 插件的配置
- 资源

你可以通过使用```<parent>```元素来继承自己的POM文件. 如下:

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
 
  <parent>
    <groupId>com.vnzmi.test</groupId>
      <artifactId>maven-test</artifactId>
      <version>1</version>
  </parent>
  <groupId>com.vnzmi.test2</groupId>
  <artifactId>my-module</artifactId>
</project>
```

如果你已经对包  ```com.vnzmi.test:maven-test:1``` 进行了安装,那么Maven可以正常工作,安装的过程其实就是将这个包按照Maven的路径规则拷贝到你本地的存储文件夹中,显然这样有点麻烦.你也可以通过 ```<relativePath>``` 元素来指定你POM的相对路径,以便Maven,每次在你对这个文件进行了更新后加载到最新内容,示例如下

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
 
  <parent>
    <groupId>com.vnzmi.test</groupId>
      <artifactId>maven-test</artifactId>
      <version>1</version>
      <relativePath>../parent/pom.xml<relativePath>
  </parent>
  <groupId>com.vnzmi.test2</groupId>
  <artifactId>my-module</artifactId>
</project>
```

## 项目聚合

项目聚合和继承有点相似,我们通过为POM设置 ```module```元素.这样在父级的POM中我们知道了他的模块,当我们在父级执行Maven命令他就能正确处理模块的执行了.

为了实现这种方式,我们需要进行两个修改

- 修改父级POM的```packaging```属性为 ```pom```,意思是打包为pom文件
- 在父级的POM里指定模块的目录

示例:

#### com.mycompany.app:my-app:1 的POM文件

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
 
  <groupId>com.mycompany.app</groupId>
  <artifactId>my-app</artifactId>
  <version>1</version>
</project>
```

#### com.mycompany.app:my-module:1 的POM文件

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
 
  <groupId>com.mycompany.app</groupId>
  <artifactId>my-module</artifactId>
  <version>1</version>
</project>
```
#### 目录结构

```sh
my-module
   |-- pom.xml
pom.xml
```

我们只需要进行在父级进行POM的修改

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
 
  <groupId>com.mycompany.app</groupId>
  <artifactId>my-app</artifactId>
  <version>1</version>
  <packaging>pom</packaging>
 
  <modules>
    <module>my-module</module>
  </modules>
</project>
```

```<module>my-module</module>```中指定的是模块的目录,如果还有下级,则按照目录进行指定即可,比如 ```<module>my-module/service</module>```, ```<module>my-module/spi</module>``` maven 查找模块会以当前路径的相对路径进行查找. 

如果他们在同级目录,目录结构如下:

```sh
my-module
   |-- pom.xml
parent
   |---pom.xml
```
则需要设置为 ```<module>../my-module</module>````,我们再parent目录执行Maven命令.

>
> 在父级执行 ```mvn package```时默认会构建所有模块.
> 我们可以通过增加参数来让Maven只构建指定的模块和他的依赖模块
> ```mvn package -pl my-module -am```
> 如果想在任意目录执行构建那就需要使用```-f```参数指定父级的POM文件地址,比如
>``` mvn -f ../pom.xml package -pl my-module -am```
> 

## 该如何使用继承和聚合

当你有一些项目他们有很多可以抽取出来的一样的配置,那么你可以使用继承,给他们指定一个```parent```来使用公共的配置.

如果你有一堆项目他们之间有依赖关系或者需要在一起构建,你可以创建一个父项目,将你的一堆项目设置为他的```module```,这样你就只需要在父项目中执行构建,你设为模块的项目也会一起被构建.Maven会自行计算他们构建的先后顺序.

作为成年人我们可能两者都要,那么你需要做的就是创建一个父POM,将你要进行配置的内容放进去,然后给他设置模块,在作为模块的每个项目的POM文件增加```parent```配置.这样既继承了配置也可以在构建时一起进行处理.具体根据你自己的项目情况进行选择.

## 项目插值和变量

在POM文件中进行可以将配置的值插入到文件中,使用如下格式

```xml
<version>${project.version}</version>
```
>
> 需要注意的是这些变量的替换是在继承之后进行处理的,如果在父项目中使用变量,然后变量在子项目中进行了定义,那么最终使用的变量并不是父项目的,而是子项目中定义的内容.
>

#### 可以使用的变量

POM中定义的所有字段都是可以作为变量进行访问的比如 ```${project.groupId}, ${project.version}, ${project.build.sourceDirectory}``` ,可以自己去POM文件进行查看.这些变量都以```project.```作为前缀.

#### 特殊变量

| 变量名 | 含义 |
| --- | --- | 
| project.basedir| 当前项目的路径|
|project.baseUri|  当前项目的URI (>= Maven 2.1.0)|
|maven.build.timestamp|  构建开始的时间戳UTC(>= Maven 2.1.0-M1)|

通过设置 ```maven.build.timestamp.format```变量来定义时间戳的格式

```xml
<project>
  ...
  <properties>
    <maven.build.timestamp.format>yyyy-MM-dd'T'HH:mm:ss'Z'</maven.build.timestamp.format>
  </properties>
  ...
</project>
```

> 
> 格式语法和Java ```SimpleDateFormat```定义一致
> 

你可以使用任意在项目中定义的属性,示例如下

```xml
<project>
  ...
  <properties>
    <mavenVersion>3.0</mavenVersion>
  </properties>
 
  <dependencies>
    <dependency>
      <groupId>org.apache.maven</groupId>
      <artifactId>maven-artifact</artifactId>
      <version>${mavenVersion}</version>
    </dependency>
    <dependency>
      <groupId>org.apache.maven</groupId>
      <artifactId>maven-core</artifactId>
      <version>${mavenVersion}</version>
    </dependency>
  </dependencies>
  ...
</project>
```







## 参考

[https://maven.apache.org/guides/introduction/introduction-to-the-pom.html](https://maven.apache.org/guides/introduction/introduction-to-the-pom.html)

[Super POM Maven 3.6.3](https://maven.apache.org/ref/3.6.3/maven-model-builder/super-pom.html)



