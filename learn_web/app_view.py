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
