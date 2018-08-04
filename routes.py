from flask import request, jsonify
from controllers import group_controller, user_controller, resource_controller, auth_controller
from app import app


def my_route(*args, **kwargs):
    """Override default @app.route decorator to default strict_slashes arg to False."""
    kwargs.setdefault('strict_slashes', False)
    return app.route(*args, **kwargs)


class Routes(object):
    @my_route('/group', methods=['POST'])
    def create_group():
        return group_controller.create(request)

    @my_route('/group/<id>', methods=['GET'])
    def get_group(id):
        return group_controller.read(request, id)

    @my_route('/group', methods=['GET'])
    def list_group():
        return group_controller.list(request)

    @my_route('/group/<id>/user', methods=['POST'])
    def add_user(id):
        return user_controller.add(request, id)

    @my_route('/group/<id>/user', methods=['GET'])
    def list_user(id):
        return user_controller.list(request, id)

    @my_route('/resource', methods=['POST'])
    def create_resource():
        return resource_controller.create(request)

    @my_route('/resource/<id>', methods=['GET'])
    def get_resource(id):
        return resource_controller.read(request, id)

    @my_route('/resource', methods=['GET'])
    def list_resource():
        return resource_controller.list(request)

    @my_route('/group/<id>/authorize', methods=['POST'])
    def auth_group(id):
        return resource_controller.add(request, id)

    @my_route('/group/<id>/resource', methods=['GET'])
    def list_resource_by_group(id):
        return resource_controller.list_by_group(request, id)

    @my_route('/authorized', methods=['GET'])
    def check_auth():
        return auth_controller.is_authorized(request)

    @app.errorhandler(404)
    def not_found(error=None):
        result = jsonify({
                'status': 404,
                'message': 'URL Not Found: ' + request.url,
        })
        result.status_code = 404
        return result

    @app.errorhandler(500)
    def internal_error(error=None):
        result = jsonify({
                'status': 500,
                'message': 'Internal Server Error!'
        })
        result.status_code = 500
        return result
