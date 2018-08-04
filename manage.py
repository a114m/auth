import os
from flask_migrate import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db


app.config.from_object(os.getenv('APP_ENV', 'config.DevelopmentConfig'))

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
