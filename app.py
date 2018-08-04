import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.getenv('APP_ENV', 'config.DevelopmentConfig'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from controllers import *


@app.route('/group', methods=['POST'], strict_slashes=False)
def create_group():
    return group_controller.create(request)


@app.route('/group/<id>', methods=['GET'], strict_slashes=False)
def get_group(id):
    return group_controller.read(request, id)


@app.route('/group', methods=['GET'], strict_slashes=False)
def list_group():
    return group_controller.list(request)


@app.route('/group/<id>/user', methods=['POST'], strict_slashes=False)
def add_user(id):
    return user_controller.add(request, id)


@app.route('/group/<id>/user', methods=['GET'], strict_slashes=False)
def list_user(id):
    return user_controller.list(request, id)


@app.route('/resource', methods=['POST'], strict_slashes=False)
def create_resource():
    return resource_controller.create(request)


@app.route('/resource/<id>', methods=['GET'], strict_slashes=False)
def get_resource(id):
    return resource_controller.read(request, id)


@app.route('/resource', methods=['GET'], strict_slashes=False)
def list_resource():
    return resource_controller.list(request)


@app.route('/group/<id>/authorize', methods=['POST'], strict_slashes=False)
def auth_group(id):
    return resource_controller.add(request, id)


@app.route('/group/<id>/resource', methods=['GET'], strict_slashes=False)
def list_resource_by_group(id):
    return resource_controller.list_by_group(request, id)


@app.route('/authorized', methods=['GET'], strict_slashes=False)
def check_auth():
    return auth_controller.is_authorized(request)


if __name__ == '__main__':
    app.run()
