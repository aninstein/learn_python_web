#!/usr/bin/env python
# -*- coding: utf-8 -*-


from werkzeug.wsgi import SharedDataMiddleware
from flask import Flask
from ext import db, jinja2_env
from utils import get_file_path


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object('config')

app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/i/': get_file_path()
})
