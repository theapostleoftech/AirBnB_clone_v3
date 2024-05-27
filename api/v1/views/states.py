#!/usr/bin/python3
"""This handles views for states"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=['GET'])
def retrieve_states_route():
    """This endpoint lists all state objects"""
    return jsonify([state.to_dict() for state in storage.all(State).values()])


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def retrieve_state_route(state_id):
    """This endpoint retrieves a state object"""
    state = storage.get(State, state_id)
    if state is not None:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_state_route(state_id):
    """This endpoint deletes a state object"""
    state = storage.get(State, state_id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def create_state_route():
    """This endpoint creates a state object"""
    state_data = request.get_json()
    if not state_data:
        abort(400, 'Not a JSON')
    elif 'name' not in state_data:
        abort(400, 'Missing name')
    new_state = State(**state_data())
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['PUT'])
def update_state_route(state_id):
    """This endpoint updates a state object"""
    state_data = request.get_json()
    if not state_data:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state is not None:
        for attr, value in state_data().items():
            setattr(state, attr, value)
        storage.save()
        return jsonify(state.to_dict()), 200
    abort(404)
