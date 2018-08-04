import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    return app


app = create_app(os.environ['APP_ENV'])
db = SQLAlchemy(app)

from routes import Routes
Routes()


if __name__ == '__main__':
    app.run()
