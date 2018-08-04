import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.getenv('APP_ENV', 'config.DevelopmentConfig'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from controllers import *


@app.route('/group', methods=['POST'])
def create_group():
    return group_controller.create(request)


@app.route('/group/<id>', methods=['GET'])
def get_group(id):
    return group_controller.read(request, id)


@app.route('/group', methods=['GET'])
def list_group():
    return group_controller.list(request)


if __name__ == '__main__':
    app.run()
