#!/usr/bin/env pythonn
# -*- coding: utf-8 -*-


from flask import Flask, url_for, request, abort, redirect
from config import setting

app = Flask(__name__)
app.config.from_object(setting)


@app.route("/")
def hello():
    return "hello world"


"""
动态url
"""
@app.route("/apple/<string:version>")
def apple(version):
    """
    动态url
    格式：<变量名称>或者<限定类型:变量名称>
    可以限定的类型包括：
    string, int, float, path(接受斜杠), uuid(只接受uuid格式的), any(可以指定多条路径，用法: <any('a', 'b'): var_name>)
    """
    return "hello %s" % version


"""
唯一url
"""
@app.route("/onlyurl/")
def onlyurl():
    """
    1. 即如果访问localhost/onlyurl, 也会被重定向到/onlyurl/
    2. 但是如果route中没有写末尾的斜杠，那么访问/onlyurl/就是404
    :return:
    """
    return "hello onlyurl"


"""
构造url
"""
@app.route("/createurl/")
def createurl():
    pass


# with app.test_request_context():  # test_request_context帮助生成上下文
#     print(url_for("createurl", id=1, name="lichangan"))
#     print(url_for("createurl", id=2))


"""
转跳和重定向
"""
@app.route("/people/")
def people():
    name = request.args.get('name')
    if not name:
        return redirect(url_for("login"))
    user_agent = request.headers.get('User-Agent')
    return 'Name: {0}, UA: {1}'.format(name, user_agent)


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        return 'User: {0} login'.format(user_id)
    elif request.method == 'GET':
        return "Open Login Page"
    else:
        abort(405)
        return "Not Page"


"""
响应
"""

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1234)
