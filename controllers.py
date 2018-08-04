from flask import jsonify
from helpers import load_body, Response
from models import db, User, Group, Resource
from sqlalchemy.exc import IntegrityError
import traceback


class GroupController(object):
    def create(self, request):
        data = load_body(request)
        if data is None:
            return Response(status=400, response={"Error": "Bad Request, request has to be a valid application-json."})
        try:
            group = Group(data["name"], data.get("description"))
            db.session.add(group)
            db.session.commit()
        except KeyError as err:
            print("Error: %s\nStacktrace: %s" % (err, traceback.format_exc()))
            db.session.rollback()
            return Response(status=400, response={
                "status": 400,
                "message": "Missing key in body"
            })
        except IntegrityError as err:
            print("Error: %s\nStacktrace: %s" % (err, traceback.format_exc()))
            db.session.rollback()
            return Response(status=400, response={
                "status": 400,
                "message": "Resource already exists"
            })
        except Exception as err:
            print("Error: %s\nStacktrace: %s" % (err, traceback.format_exc()))
            db.session.rollback()
            return Response(status=500, response={
                "status": 500,
                "message": "Internal Server Error"
            })
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
        query = Group.query
        count = query.count()

        items = map(lambda group: {
            "id": group.id,
            "name": group.name,
            "description": group.description,
        }, query.all())
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
                user = User.query.get(user_id)  # XXX: if single query is executed each loop then ehance to execute one query using filters
                if not user:
                    user = User(id=user_id, groups=[group_id])
                    db.session.add(user)
                else:
                    users.append(user)
            for user in users:
                if group_id not in user.groups:
                    user.groups = user.groups + [group_id]
        except KeyError as err:
            print("Error: %s\nStacktrace: %s" % (err, traceback.format_exc()))
            db.session.rollback()
            return Response(status=400, response={
                "status": 400,
                "message": "Missing key in body"
            })
        except IntegrityError as err:
            print("Error: %s\nStacktrace: %s" % (err, traceback.format_exc()))
            db.session.rollback()
            return Response(status=400, response={
                "status": 400,
                "message": "Resource already exists"
            })
        except Exception as err:
            print("Error: %s\nStacktrace: %s" % (err, traceback.format_exc()))
            db.session.rollback()
            return Response(status=500, response={
                "status": 500,
                "message": "Internal Server Error"
            })
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
    def create(self, request):
        data = load_body(request)
        if data is None:
            return Response(status=400, response={
                "status": 400,
                "message": "Bad Request, request has to be a valid application-json."
            })
        try:
            resource = Resource(name=data["name"], groups=data.get("groups", []))
            db.session.add(resource)
            db.session.commit()
        except KeyError as err:
            print("Error: %s\nStacktrace: %s" % (err, traceback.format_exc()))
            db.session.rollback()
            return Response(status=400, response={
                "status": 400,
                "message": "Missing key in body"
            })
        except IntegrityError as err:
            print("Error: %s\nStacktrace: %s" % (err, traceback.format_exc()))
            db.session.rollback()
            return Response(status=400, response={
                "status": 400,
                "message": "Resource already exists"
            })
        except Exception as err:
            print("Error: %s\nStacktrace: %s" % (err, traceback.format_exc()))
            db.session.rollback()
            return Response(status=500, response={
                "status": 500,
                "message": "Internal Server Error"
            })
        else:
            result = {
                "id": resource.id,
                "name": resource.name,
            }
            return jsonify(result)

    def read(self, request, id):
        resource = Resource.query.get_or_404(id)
        result = {
            "id": resource.id,
            "name": resource.name,
        }
        return jsonify(result)

    def list(self, request):
        query = Resource.query
        count = query.count()

        items = map(lambda resource: {
            "id": resource.id,
            "name": resource.name,
        }, query.all())
        result = {
            "count": count,
            "items": list(items)
        }
        return jsonify(result)

    def add(self, request, group_id):
        Group.query.get_or_404(group_id)
        try:
            group_id = int(group_id)
            data = load_body(request)
            resources_ids = map(lambda item: item['resourceId'], data)
            resources = list()
            for resource_id in resources_ids:
                resource = Resource.query.get(resource_id)  # XXX: if single query is executed each loop then ehance to execute one query using filters
                if not resource:
                    Resource.query.session.rollback()
                    return Response(status=404, response={
                        "status": 404,
                        "message": "Resource Not Found, resourceId: %s" % resource_id
                    })
                else:
                    resources.append(resource)
            for resource in resources:
                if group_id not in resource.groups:
                    resource.groups = resource.groups + [group_id]
        except KeyError as err:
            print("Error: %s\nStacktrace: %s" % (err, traceback.format_exc()))
            db.session.rollback()
            return Response(status=400, response={
                "status": 400,
                "message": "Missing key in body"
            })
        except IntegrityError as err:
            print("Error: %s\nStacktrace: %s" % (err, traceback.format_exc()))
            db.session.rollback()
            return Response(status=400, response={
                "status": 400,
                "message": "Resource already exists"
            })
        except Exception as err:
            print("Error: %s\nStacktrace: %s" % (err, traceback.format_exc()))
            db.session.rollback()
            return Response(status=500, response={
                "status": 500,
                "message": "Internal Server Error"
            })
        else:
            db.session.commit()
            return Response(status=204)

    def list_by_group(self, request, group_id):
        Group.query.get_or_404(group_id)
        q = Resource.query.filter(Resource.groups.contains(group_id))
        count = q.count()
        items = map(lambda resource: {
            "id": resource.id,
            "name": resource.name,
        }, q.all())
        result = {
            "count": count,
            "items": list(items)
        }
        return jsonify(result)


class AuthController(object):
    def is_authorized(self, request):
        try:
            user_id = request.args['userId']
            resource_name = request.args['resourceName']
        except KeyError:
            return Response(status=400, response={
                "status": 400,
                "message": "Missing query param 'userId' or 'resourceName'"
            })

        user = User.query.get(user_id)
        resource = Resource.query.filter(Resource.name == resource_name).first()
        if user is None or resource is None:
            return Response(status=400, response={"error": "Invalid 'userId' or 'resourceName'"})

        is_authorized = not set(user.groups).isdisjoint(resource.groups)  # check if both user and resource has relation with the same group

        return Response(response={"authorized": is_authorized}, status=200 if is_authorized else 403)


group_controller = GroupController()
user_controller = UserController()
resource_controller = ResourceController()
auth_controller = AuthController()
