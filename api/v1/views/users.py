#!/usr/bin/python3
"""This holds views for the user objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False,
                 methods=['GET'])
def retrieve_users_route():
    """This endpoint lists all users"""
    return jsonify([user.to_dict() for user in storage.all(User).values()])


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=['GET'])
def retrieve_user_route(user_id):
    """This endpoint retrieves the user object"""
    user = storage.get(User, user_id)
    if user is not None:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_user_route(user_id):
    """This endpoint deletes the user object"""
    user = storage.get(User, user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/users", strict_slashes=False,
                 methods=['POST'])
def create_user_route():
    """This endpoint creates a user object"""
    user_data = request.get_json()
    if not user_data:
        abort(400, 'Not a JSON')
    if 'email' not in user_data:
        abort(400, 'Missing email')
    if 'password' not in user_data:
        abort(400, 'Missing password')
    new_user = User(**user_data())
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=['PUT'])
def update_user_route(user_id):
    """This endpoint updates the user object"""
    user_data = request.get_json()
    if not user_data:
        abort(400, 'Not a JSON')
    user = storage.get(User, user_id)
    if user is not None:
        for attr, value in user_data().items():
            if ((hasattr(user, attr)
                and attr != 'id'
                and attr != 'created_at'
                and attr != 'updated_at')
                    and attr != 'email'):
                setattr(user, attr, value)
        storage.save()
        return jsonify(user.to_dict()), 200
    abort(404)
