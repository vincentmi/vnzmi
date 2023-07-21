---
layout:     post
title:      "使用Flask开发应用程序"
date:       "2023-07-21 10:44:00"
author:     "Vincent"
image:  "/img/erhai18622_0_1.jpg"
catalog: true
tags:
    - python
    - flask
---

# 安装FLASK

先安装Pyhton，[https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/)

FLASK支持 3.8+版本的python

为啥不用Django ,由于目前前后端分离，Django的很多功能用不上，Flask更简单小巧一点。

## 配置虚拟环境

使用虚拟环境可以将你的项目依赖和其他项目进行隔离，更好的进行依赖管理，使用venv工具来进行管理。

```sh
mkdir qa-panel
 cd qa-panel
 python3 -m venv .venv

```

## 激活虚拟环境

```sh
chmod a+x ./.venv/bin/activate
 ./.venv/bin/activate
```
## 安装flask

```sh
pip install Flask
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Requirement already satisfied: Flask in /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages (2.3.2)
....
```

# 目录结构

Flask 项目可以只简单的包含一个文件：

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'
```

```sh
flask --app hello run
```

然后浏览器访问 [http://127.0.0.1:5000](http://127.0.0.1:5000) 就可以看到你的第一个Flask应用程序了。

随着项目的增大，我们不可能把代码都放到一个文件里。所以python使用package来对代码进行组织在需要的时候才进行导入。

根据社区各位大佬的经验和建议，Flask应用推荐如下项目结构：

- ```flaskr``` 目录，一个python的包，包含你的应用的代码和相关文件。
- ```tests``` 目录，包含测试代码
- ```.venv``` python 虚拟环境的目录，Flask和他的依赖安装到这里
- ```.git``` GIT版本控制配置目录
- 其他文件比如： .gitignore , README.md ，应用配置文件等项目相关文件

最后目录大概如下：

```
/home/user/Projects/qa-panel
├── flaskr/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   ├── auth.py
│   ├── blog.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── blog/
│   │       ├── create.html
│   │       ├── index.html
│   │       └── update.html
│   └── static/
│       └── style.css
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_blog.py
├── .venv/
├── pyproject.toml
└── MANIFEST.in
```

如果使用 git 进行代码管理，可以增加如下忽略文件配置：

.gitignore

```
.venv/

*.pyc
__pycache__/

instance/

.pytest_cache/
.coverage
htmlcov/

dist/
build/
*.egg-info/
```

# 应用配置

Flask 应用就是一个 Flask 类的实例，应用的各种配置包含路由信息等都需要注册到该实例，因此这个对象是我们的核心，我们需要很容易的访问该对象，因此我们可以使用应用工厂来实现这个。通过在一个函数中完成我们需要对这个应用实例进行的各种配置，最后返回他。

## 创建我们的应用包 

```sh
mkdir flaskr 
```

在包目录创建 ```__init__.py```文件，编写工厂方法：

```flaskr/__init__.py```

```python
import os

from flask import Flask

def create_app(test_config=None):
    # 创建Flask对象，设置加载
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # 加载配置文件
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 加载测试配置
        app.config.from_mapping(test_config)

    # 创建必要的目录
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 注册一个简单的路由
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
```

- ```app = Flask(__name__, instance_relative_config=True) ```  创建Flask对象
 - ```__name__``` 是当前模块的名称，用于让App设置一些路径相关的内容
 - ```instance_relative_config=True```  告诉应用从实例的相当路径加载配置文件，这样一些配置文件可以放置到外部，不用放入包中。也可以避免将配置文件放入到版本库中造成信息泄漏。
- ```app.config.from_mapping() ``` 设置一些默认配置
    - ```SECRET_KEY``` 用于加密的字符串 ，部署时需要更换成更安全的字符串，目前简单设置成```dev```.
    - ```DATABASE``` 使用sqlite 数据库，指定数据库文件的路径，通常正式点的项目我们会使用MySQL等数据库
- ```app.config.from_pyfile() ``` 从 ```config.py```加载配置覆盖掉默认配置。
- ```os.makedirs()``` 确保 ```app.instance_path```文件夹存在， Flask 不会帮我们创建这个文件夹, 但是我们配置了SQLite 文件要存在这里，因此我们得自己创建目录。这一步并不是必须的，如果我们使用MySQL就没这个烦恼。这一步只是演示我们如果需要在应用中进行一些初始操作可以这样处理。

- @app.route() 创建了一个简单的路由 ```/hello```，定义了一个函数返回了一些响应，这里是一个字符串   'Hello, World!' 

## 运行我们的程序

现在我们可以使用 ```flask```命令来运行我们的应用。在终端进入我们项目的主目录执行以下命令：

```sh
flask --app flaskr run --debug
```

输出内容类似：

```sh
 * Serving Flask app 'flaskr'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
flaskr
 * Debugger is active!
 * Debugger PIN: 354-025-273
```
 
然后浏览器访问 [http://127.0.0.1:5000](http://127.0.0.1:5000) 就可以看到你的大型Flask应用程序了。

>  如果默认的 ```5000``` 端口被其他程序占用，会出现这个错误，```OSError: [Errno 98] or OSError: [WinError 10013]```
> 此时你需要使用一些命令行的参数来修改运行的端口

该命令还有一些有用的参数：

- ```--debug / --no-debug``` 是否开启调试
-  ``` -p, --port INTEGER``` 指定运行的端口号。
-  ``` -h, --host TEXT``` 指定绑定网络接口，设置```0.0.0.0```是绑定到当前服务器的所有IP上。

还有其他的 参数可以使用 ```flask run --help```查看

我们稍微修改下命令参数:

```sh
flask --app flaskr  run -h 0.0.0.0 --debug   -p 18622
```

输出内容如下：

```
  * Serving Flask app 'flaskr'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:18622
 * Running on http://10.12.4.55:18622
Press CTRL+C to quit
 * Restarting with stat
flaskr
 * Debugger is active!
 * Debugger PIN: 354-025-273
```

端口已经改变成我们设置的端口了。


# 数据库访问

我们先使用SQLlite数据库来看看如何初始化一些资源。python内建了sqlite3 模块。我们使用这个模块来进行一些数据的保存。使用SQLite 可以不用启动独立的数据库服务器，比较适合小型的应用和嵌入式设备等。

## 连接数据库

```flaskr/db.py```文件


```py
import sqlite3

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
```

 - ```g``` 是一个特殊对象，每一次请求会初始化一次。我们使用```g``` 对象在一次访问中存储了数据库连接。当一个请求中多次调用 ```get_db```的时候就不用重复创建 数据库连接了。
 - ```current_app``` 是另一个特殊对象，指向当前正在处理该请求的Flask应用程序。可以理解这是本次请求的上下文。因为我们使用了应用工厂模式，所以现在并没有一个应用对象。```get_db```将在应用被创建的时候调用，所以我们使用这个对象.
- ```sqlite3.connect() ```  使用 ```DATABASE``` 设置的路径，简历数据库连接. 稍后我们会初始化这个数据文件。
- ```sqlite3.Row``` 设置查询结果返回的类型，我们设置返回Dict，可以使用栏位名访问列内容。


## 创建数据表









