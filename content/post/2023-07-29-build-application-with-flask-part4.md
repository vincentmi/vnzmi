---
layout:     post
title:      "使用Flask开发应用程序（4）- 使用SQLAlchemy "
date:       "2023-07-29 10:44:00"
author:     "Vincent"
image:  "/img/post-bg-python.png"
catalog: true
tags:
    - python
    - flask
    - sqlalchemy
---

# ORM 

ORM 对象关系映射，通过将数据库映射到业务对象中，可以简化对数据库的操作，提高开发效率。我们把我们的应用改造成使用ORM来实现数据库交互。

# SQLAlchemy

[https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)

[https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)


# 安装

使用Flask-SQLAlchemy为Flask集成了SQLAlchemy.

```sh
pip install -U Flask-SQLAlchemy
```

## 配置

SQLAlchemy 最少只需要一个配置项 ```SQLALCHEMY_DATABASE_URI```,用于建立数据库连接。在对Flask应用程序完成初始化之后可以调用 ```SQLAlchemy.init_db```方法完成数据库链接的初始化。
我们在初始化应用的时候进行相关的配置。

```__init__.py```

```py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flaskr_orm.db"
# initialize the app with the extension
db.init_app(app)
```

```db```对象用于访问 ```db.Model``` 访问数据模型，```db.session```用于执行SQL语句。

## 定义模型 

```py
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
```
