#!/usr/bin/env python
# -*- coding: utf-8 -*-


from jinja2 import Template, Environment, PackageLoader


def fun1():
    """
    使用模板的方法1
    """
    temp = Template('Hello {{ name }}')
    print(temp.render(name='lichangan'))


def fun2():
    """
    使用模板的方法2，使用env，其实方法1也是使用env，封装了一层而已
    """
    env = Environment()
    temp = env.from_string('Hello {{ name }}')
    print(temp.render(name='zhuangruiying'))


def fun3():
    """
    使用模板的方法3，从template文件夹读取模板文件
    :return:
    """
    env = Environment(loader=PackageLoader('template_jinja2', 'jinja2_file'))
    temp = env.get_template('simple.html')
    valus = {
        "items": [{
            "href": "www.lichangan.com",
            "caption": '李昌安的个人网站'
        }],
        "title": "个人网站",
        "content": "牛逼的个人网站"
    }
    print(temp.render(**valus))


if __name__ == '__main__':

    # fun1()
    # fun2()
    fun3()
