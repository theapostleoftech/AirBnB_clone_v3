#!/usr/bin/python3
"""This holds routes for the state objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=['GET'])
def states_route():
    """This endpoint retrieves all state object"""
    return jsonify([state.to_dict() for state in storage.all(State).values()])


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def get_state_id_route(state_id):
    """This endpoint lists a state object"""
    state_by_id = storage.get(State, state_id)
    if state_by_id is not None:
        return jsonify(state_by_id.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_state_id_route(state_id):
    """This endpoint deletes a state object"""
    state_by_id = storage.get(State, state_id)
    if state_by_id is not None:
        storage.delete(state_by_id)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def post_state_route():
    """This endpoint creates a state object"""
    json_req = request.get_json()
    if not json_req:
        abort(400, 'Not a JSON')
    elif 'name' not in json_req:
        abort(400, 'Missing name')
    new_state = State(**request.get_json())
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['PUT'])
def put_state_id_route(state_id):
    """This endpoint updates the state object"""
    json_req = request.get_json()
    if not json_req:
        abort(400, 'Not a JSON')
    state_by_id = storage.get(State, state_id)
    if state_by_id is not None:
        for attr, value in request.get_json().items():
            setattr(state_by_id, attr, value)
        storage.save()
        return jsonify(state_by_id.to_dict()), 200
    abort(404)
