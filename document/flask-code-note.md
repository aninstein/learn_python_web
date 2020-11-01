# flask学习代码记录
---
---
# （一）接收请求
## 1. 视图
视图主要是MVT(model, view, template)框架里面的
- model, 数据模型，主要是指数据库模型
- view, 接受请求 处理请求 返回数据
- template, html页面
比起app.route，视图能够支持继承，并且业务与url分离
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, jsonify
from flask.views import MethodView


app = Flask(__name__)


class UserAPI(MethodView):

    def get(self):
        return jsonify({
            'username': 'flask',
            'avater': 'www.lichangan.com'
        })

    def post(self):
        return 'hello world!'


app.add_url_rule('/user', view_func=UserAPI.as_view('userview'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)

```
上述代码：
1. 继承==MethodView==类可以重载，get/post/delete/put的请求方法。来实现针对某一类请求的视图接收。
2. 使用===add_url_rule==方法来构造与视图关联的请求url
3. 继承自模板的as_view方法可以将类转化为实际的视图类

## 2. 蓝图
蓝图主要实现了页面的不同模块的请求来进行不同的路由部分代码的编写，主要是基于web应用页面的组织划分的蓝图。
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Blueprint, Flask


user_bp = Blueprint('user', __name__, url_prefix='/user')
admin_bp = Blueprint('admin', __name__)


@user_bp.route("/")
def user():
    return 'User index page!'


@admin_bp.route("/")
def admin():
    return 'Admin index page!'


app = Flask(__name__)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8510, debug=True)
```
上述代码：
1. 分别定义了两个蓝图user_bp和admin_bp，并且定义了对应蓝图“/”的路由。
2. 在app中使用register_blueprint来注册蓝图
3. 注意url_prefix既可以放在定义，也可以放在注册时候，非常方便


## 3. 蓝图和视图
两者的关系可以这么理解：

一个或多个Blueprint构成一个应用，
一个或多个Pluggable Views构成一个Blueprint，

前者关注于应用程序级别的结构，
后者关注一个响应的实现细节。

在不需要Blueprint的情况下，可以由PluggableView构成简单应用。

PluggableView属于类结构，与普通视图响应函数相比，可以在同一个URL的不同的Method响应时重用代码。
例如：
一个Form往往有get和post两种操作，用PluggableView子类的get和post函数分别响应，把两者共用的逻辑在类的其它函数中实现从而重用。
如果用函数直接响应，就需要额外的方式来实现共享逻辑，在这过程中，会涉及到request,http状态等一系列相关对象的传递等细节，用类则避免了这些细节。


# （二）模板
## 1. jinjia2模板
在么MVT模型当中，我们一般使用jinja2处理template层，html的东西，jinja2模板比Make能够比较有足够的分离前后端逻辑。
