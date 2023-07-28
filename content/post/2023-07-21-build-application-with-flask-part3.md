---
layout:     post
title:      "使用Flask开发应用程序（3）- 测试和部署"
date:       "2023-07-21 10:44:00"
author:     "Vincent"
image:  "/img/erhai18622_0_1.jpg"
catalog: true
tags:
    - python
    - flask
---

# 让应用可安装

让应用可安装可以让我们很方便的在不同环境快速部署我们的应用，让应用能像Flask一样进行安装和测试

## pyproject.toml 项目描述文件

```pyproject.toml ``` 用于描述项目如果运行和安装

```pyproject.toml```

```toml
[project]
name = "flaskr"
version = "1.0.0"
description = "简单的博客系统"
dependencies = [
    "flask",
]

[build-system]
requires = ["flit_core<4"]
build-backend = "flit_core.buildapi"
```

[查看pyproject.toml详细说明](https://packaging.python.org/en/latest/tutorials/packaging-projects/#creating-the-package-files)


## 安装测试

```sh
pip install -e .
```

使用该命令会在当前目录查询 ```pyproject.toml```并将应用安装为可编辑的项目。我们可以对项目进行修改。但是我们可以在任何地方使用 ```flask --app flask run ``` 而不用一定要到该目录才能执行。我们的修改也会影响到所有运行的应用。你可以使用 ```pip list``` 列出所有已经安装的应用。


# 单元测试

我们将使用 ```pytest```和```coverage```进行单元测试和测试覆盖计算。通过pip进行安装

```sh
pip install pytest coverage
```

## 测试准备

测试代码放在项目根目录的 ```tests```文件夹。```tests/conftest.py``` 包含测试的配置函数。所有测试都以 ```test_``` 作为模块的前缀。每个测试都需要初始数据。初始数据通过SQL来进行初始化。

```tests/data.sql```

```sql
INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO post (title, body, author_id, created)
VALUES
  ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00');
```


```tests/conftest.py```

```py
import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

#打开初始化数据文件读取到变量
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

#初始化APP对象
@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
```

- ```db_fd, db_path = tempfile.mkstemp()``` 创建一个临时文件，返回文件资源描述符和路径。用这个文件来存放测试的数据。```os.unlink(db_path)``` 测试运行完后该文件被删除了。保证每次测试都是干净的数据。

- ```TESTING``` 配置 Flask 当前应用是在测试模式. Flask 会针对测试进行内部行为的修改。其他扩展也使用该标识来修改自己的行为。

```app.test_client()```使用应用对象创建一个测试架，测试时会使用这个对象在创建客户端请求，而不用启动一个服务器。

```test_cli_runner()``` 和 ```app.test_client()``` 类似，只是调用的是命令行应用程序。

```Pytest```通过匹配测试函数中参数的名字来匹配 fixture 的名字，从而调用到合适的客户端。例如：```test_hello(client,name="Vincent")```,他有一个 ```client```参数，那么他就会匹配到 ```client``` fixture. 调用他并返回给测试函数作为参数。

## 测试工厂函数

工厂函数的没有太大必要进行单独测试，因为会被很多测试调用，最多测试下一些加载了的不同配置。

```tests/test_factory.py```

```py
from flaskr import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
```
```test_hello``` 测试函数使用```client```发送了一个请求，检查请求与期望的结果是否相同。

## 测试数据库

数据库函数在应用的每次调用中应该返回同一个连接。应用执行完成后应该进行关闭。

```tests/test_db.py```

```py
import sqlite3

import pytest
from flaskr.db import get_db

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)
```
```init-db```命令应该调用```init_db```函数并输出一些内容。 

```tests/test_db.py```

```py
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
```

```monkeypatch.setattr``` 设置了一个伪造的函数来代替```init_db```函数。通过这个测试我们可以了解到```init_db```命令调用后正常的调用了 ```init_db```函数。


## 测试授权

大部分的视图我们都会要求用户登录后才能访问。我们手动发送一个请求进行登录就可以实现，我们可以编写这个函数然后通过 fixturec传递到每个测试。

```tests/conftest.py```

```py
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)

```

#### 测试注册

```tests/test_auth.py```

```py
import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data
```

```client.post```发送一个POST请求，```client.get```发送一个GET类型的请求。如果要检查一个请求是否成功，只需要检查响应的```status_code```是不是``‵200```。

```response.headers``` 返回响应的头信息，测试中我们判断了头的```Location```字段是否和我们期望的一致。

```response.data``` 包含了字节类型的响应内容，如果你要获取文本进行比较，使用 ```get_data(as_text=True)```

```pytest.mark.parametrize``` 告诉```Pytest```使用不同参数调用这个测试函数，这样就不用写多几次了。

#### 测试登录

```py
def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session

```

登出执行后检查Session来确定是否成功登出。

## 测试文章 

文章的测试因为涉及到登录后操作，因此我们要使用之前编写的 ```auth``` fixture.

```test_post.py```

```py
import pytest
from flaskr.db import get_db

def test_index(client, auth):
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data
```

如果用户没有登录去访问某些功能会报404或者403错误，这些情况我们也要进行测试。

```py
@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404
```

其他的大同小异。

参见 [https://github.com/vincentmi/qa-panel/blob/main/tests/test_post.py](https://github.com/vincentmi/qa-panel/blob/main/tests/test_post.py)


## 运行测试


针对测试的配置项，定义一些目录的信息

```pyproject.toml```

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.coverage.run]
branch = true

```

在项目根目录执行

```sh
pytest
```

来运行单元测试。


计算测试覆盖

```sh
coverage run -m pytest
```

计算测试覆盖

```sh
# 展示简单的报告
coverage report

# 生成HTML报告
coverage html
```

生成的报告在 ```./htmlcov/index.html ```


# 部署到生产环境

现在我们的应用已经开发完成可以部署到生产环境。

## 构建

为了更方便的部署我们将应用打包成 wheel文件包。安装打包工具```pip install build```

```sh
$ python3 -m build --wheel
* Creating venv isolated environment...
* Installing packages in isolated environment... (flit_core<4)
* Getting build dependencies for wheel...
* Building wheel...
Successfully built flaskr-1.0.0-py2.py3-none-any.whl
```

打包好的文件在```./dist/flaskr-1.0.0-py2.py3-none-any.whl``` ，文件名格式为 ``` {project name}-{version}-{python tag} -{abi tag}-{platform tag}```

在新的机器上创建虚拟环境，然后执行
```pip install flaskr-1.0.0-py3-none-any.whl```安装应用，
执行 ```flask --app flaskr init-db```初始化数据库。

执行成功后会在虚拟环境产生一个目录 ```.venv/var/flaskr-instance ``` 用于存储数据。


生成环境我们需要配置足够复杂的Secert避免加密数据被破解。增加一个配置文件

```config.py```

```py
SECRET_KEY = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
```

> 使用python命令可以生成一个随机字符串 ```$ python -c 'import secrets; print(secrets.token_hex())'```
> '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'



## 部署到生产型WebServer

```flask run```命令启动的WebServer仅仅用于方便开发时进行调试和预览。对于生产环境的高吞吐量和大流量访问是无法稳定支持的。因此我们需要选择专业WSGI应用服务来部署我们的应用。有很多用于生产的WSGI服务器，[https://flask.palletsprojects.com/en/2.3.x/deploying/](https://flask.palletsprojects.com/en/2.3.x/deploying/),我们目前选择```waitress```

先安装

```sh
pip install waitress
```

然后部署：

```sh
waitress-serve --call 'flaskr:create_app'
```



