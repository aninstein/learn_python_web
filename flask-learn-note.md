# flask学习笔记
---
---
## 1. 搭建环境
### 1.1 虚拟环境（使用==pipenv==）
使用pipenv搭建虚拟环境，来代替原来的virtualenv+requirement.txt的方式，完成虚拟环境的搭建。
在项目的根目录，安装虚拟环境命令，随后会生成==Pipfile==：
```
pip install pipenv
```
执行命令之后，在会在~/.local/share/virtualenvs/目录下创建虚拟环境文件夹

- ==pipenv install== 创建虚拟环境
- ==pipenv shell== 显示激活虚拟环境
- ==pipenv run== 如pipenv run python hello.py，可以用虚拟环境运行hello.py
- 与传统的requirement.txt手动维护的依赖包不同，pipenv在install之后会产生一个Pipfile文件
- ==pipenv graph== 查看依赖情况
- ==pipenv install \<pkg>== 安装pip包到虚拟环境，可以使用此命令安装flask：==pipenv install flask==
- ==pipenv update== 更新python包
## 2. hello world
### 2.1 hello world代码如下
代码文件'run_app.py'
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request


app = Flask(__name__)


@app.route("/")
def hello():
    return "hello world！"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1234, debug=True)
```
### 2.2 flask代码开发服务器
#### 2.2.1 直接通过python运行
```
python run_app.py
```
#### 2.2.2 使用flask内置的测试服务器启动
注意：文件名称默认必须是‘app.py’或者‘wsgi.py’，可以通过==FLASK_APP==字段设置运行文件名称
比如'run_app.py'：
```
export FLASK_APP=run_app
```
不同的app可能有不同的环境变量，则可以使用python-dotenv管理环境变量，我们这里使用的pipenv，普通环境就使用pip即可
```
pipenv install python-dotenv
```
flask run默认只开启127.0.0.1，端口是5000
```
flask run
```
#### 2.2.3 验证
在浏览器输入：
```
http://127.0.0.1:1234
```
## 3. 登陆页面
## 4. 表单验证
## 5. 前后台交互
## 6. mysql数据集合
## 7. 安全能力
## 8. 部署方式
## 9. 高可用
## 10. 可视化