#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
存放拓展的封装
"""
from jinja2 import Environment, PackageLoader
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
jinja2_env = Environment(loader=PackageLoader('app', 'templates'))
