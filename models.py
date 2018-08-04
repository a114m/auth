from app import db
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(24), primary_key=True)
    groups = db.Column(JSON)

    def __init__(self, id, groups=None):
        self.id = id
        self.groups = groups if groups is not None else list()

    def __repr__(self):
        return '<User: {} groups: {}>'.format(self.id, self.groups)


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), index=True, unique=True)
    description = db.Column(db.String())

    def __init__(self, name, description=""):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Group {} id: {}>'.format(self.name, self.id)


class Resource(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), index=True, unique=True)
    groups = db.Column(JSON)

    def __init__(self, name, groups=None):
        self.name = name
        self.groups = groups if groups is not None else list()

    def __repr__(self):
        return '<Resource: {} id: {}>'.format(self.name, self.id)
