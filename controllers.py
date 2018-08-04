from flask import abort, jsonify
from app import db
from helpers import load_body
from models import *


class GroupController(object):
    def create(self, request):
        data = load_body(request)
        group = Group(data["name"], data["description"])
        try:
            db.session.add(group)
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(400)
        else:
            result = {
                "id": group.id,
                "name": group.name,
                "description": group.description,
            }
            return jsonify(result)

    def read(self, request, id):
        group = Group.query.get_or_404(id)
        result = {
            "id": group.id,
            "name": group.name,
            "description": group.description,
        }
        return jsonify(result)

    def list(self, request):
        count = Group.query.count()

        def serialize_group(group):
            return {
                "id": group.id,
                "name": group.name,
                "description": group.description,
            }
        items = map(serialize_group, Group.query.all())
        result = {
            "count": count,
            "items": list(items)
        }
        return jsonify(result)


class UserController(object):
    pass


class ResourceController(object):
    pass


group_controller = GroupController()
user_controller = UserController()
resource_controller = ResourceController()
