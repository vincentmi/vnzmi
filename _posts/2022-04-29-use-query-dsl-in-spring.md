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

## 使用QueryDSL 

APT 插件可以根据JPA Entity生成查询对象```User.java```对应 ```QUser.java```.

如果您的Entity 继承了使用```@MappedSuperclass```基础类.例如:

BaseEntity.java

```java
@MappedSuperclass
public abstract class BaseEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @ApiModelProperty("主键")
    private Long id;
    @CreationTimestamp
    @ApiModelProperty("创建时间")
    private LocalDateTime createdAt;
    @UpdateTimestamp
    @ApiModelProperty("更新时间")
    private LocalDateTime updatedAt;

    public Long getId() {
        return id;
    }

    public BaseEntity setId(Long id) {
        this.id = id;
        return this;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public BaseEntity setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
        return this;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public BaseEntity setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
        return this;
    }
}
```

Device.java

```java
@Entity
@Data
public class Device  extends BaseEntity {
    private String code;
    private Long gatewayId;
    private Long typeId;
    private Long subtypeId;
    private String name;
    private Long brandId;
    private String modelNo;
    private String serialNo;
    private String uuid;
    private Long operatorId;
    private String latitude;
    private String longitude;
    private String geohash;
    private Boolean isOnline;
    private Boolean isHide;
    private Boolean isActive;
}
```

生成的代码会出现缺失类的情况,这时候需要在主包增加```package-info.java```
使用```@QueryEntities```包注解指定该class.

```java 
@QueryEntities(value= BaseEntity.class)

package com.xxx.platform;
import com.xxx.platform.common.repository.BaseEntity;
import com.querydsl.core.annotations.QueryEntities;

```

## 使用QueryDSL进行查询

示例如下:

进行联表查询,并将结果映射到POJO中

```java 
@Override
public Page<DeviceInfoVO> listQueryDSL(DeviceQueryDTO queryDTO, Pageable pageable) {

    QDevice device = QDevice.device;
    QBrand brand = QBrand.brand;
    QSubtype subtype = QSubtype.subtype;
    JPAQuery<DeviceInfoVO> query = jpaQueryFactory.from(device)
            .select(Projections.bean(DeviceInfoVO.class , device.name.as("name"),subtype.name.as("subtypeName") , brand.name.as("brandName")))
            .leftJoin(brand).on(device.brandId.eq(brand.id))
            .leftJoin(subtype).on(device.subtypeId.eq(subtype.id));


    log.info("{} , {} ,-> {}",query,query.fetchCount(),query.fetch());
    Page<DeviceInfoVO> data = (Page<DeviceInfoVO>)deviceRepository.findAll(query,pageable);
    return data;
}
```

可以对```BaseRepository```进行扩展增加对QueryDSL分页的支持

```java
package com.xxx.platform.common.repository;


import com.heroera.common.exception.ApiException;
import com.heroera.common.exception.ErrorCode;
import com.querydsl.jpa.impl.JPAQuery;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.support.JpaEntityInformation;
import org.springframework.data.jpa.repository.support.SimpleJpaRepository;
import org.springframework.transaction.annotation.Transactional;

import javax.persistence.EntityManager;
import java.util.List;

public class BaseRepositoryImpl<T extends BaseEntity,ID> extends  SimpleJpaRepository<T,ID> implements BaseRepository<T,ID> {

    protected  EntityManager entityManager;

    public BaseRepositoryImpl(JpaEntityInformation<T, ?> entityInformation, EntityManager entityManager) {
        super(entityInformation, entityManager);
        this.entityManager = entityManager;
    }

    public BaseRepositoryImpl(Class<T> domainClass, EntityManager em) {
        super(domainClass, em);
    }

    @Override
    public T findByIdOrFail(ID id) {
        return findById(id).orElseThrow(() -> new ApiException(ErrorCode.ENTITY_NOT_FOUND));
    }

    @Override
    public T findByIdOrNull(ID id) {
        return findById(id).orElse(null);
    }

    @Override
    @Transactional
    public void deleteByIdList(Iterable<ID> idList) {
        List<T> entityList = findAllById(idList);
        deleteInBatch(entityList);
    }

    @Override
    public Page<?> findAll(JPAQuery<?> query, Pageable pageable) {
        long total = query.fetchCount();

        query.offset(pageable.getPageNumber() * pageable.getPageSize()).limit(pageable.getPageSize());

        Page<?> pageData = new PageImpl<>(query.fetch(),pageable,total);
        return pageData;
    }
}

```

QueryDSL 可以对JPA进行补充,在进行复杂查询时非常好用.这是另一个你换掉MyBatis的理由 ;)

