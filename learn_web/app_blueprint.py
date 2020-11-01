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
