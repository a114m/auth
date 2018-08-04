from flask import abort, jsonify, Response
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
    def add(self, request, group_id):
        try:
            group_id = int(group_id)
            data = load_body(request)
            users_ids = map(lambda item: item['userId'], data)
            users = list()
            for user_id in users_ids:
                user = User.query.get(user_id)  # TODO: check if
                if not user:
                    user = User(id=user_id, groups=[group_id])
                    db.session.add(user)
                else:
                    users.append(user)
            for user in users:
                if group_id not in user.groups:
                    user.groups = user.groups + [group_id]
        except Exception:
            db.session.rollback()
            abort(400)
        else:
            db.session.commit()
            return Response(status=204)

    def list(self, request, group_id):
        q = User.query.filter(User.groups.contains(group_id))
        count = q.count()
        items = map(lambda u: {
            "userId": u.id
        }, q.all())
        result = {
            "count": count,
            "items": list(items)
        }
        return jsonify(result)


class ResourceController(object):
    pass


group_controller = GroupController()
user_controller = UserController()
resource_controller = ResourceController()
