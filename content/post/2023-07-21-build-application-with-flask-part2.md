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

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


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