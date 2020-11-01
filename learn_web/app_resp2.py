#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, jsonify
from werkzeug.wrappers import Response
from config import setting

app = Flask(__name__, static_folder='/web_ui')
app.config.from_object(setting)

"""
另一种响应的方法
使用werkzeug内置的Response进行返回，使用jsonify进行json的格式化返回
"""
class JSONResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(JSONResponse, cls).force_type(rv, environ)


def set_response_class():
    app.request_class = JSONResponse

set_response_class()


@app.route("/json_hello/")
def json_hello():
    return {"message": 'hello world!'}


@app.route("/json_headers")
def json_headers():
    return {"header": [1, 2, 3]}, 201, [('X-Request-Id', '100')]


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=1235)
