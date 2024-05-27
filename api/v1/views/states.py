#!/usr/bin/python3
"""This handles views for states"""

from flask import abort, jsonify, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_states_route():
    """This endpoint lists all state objects"""
    states = storage.all(State).values()
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<string:state_id>',
                 methods=['GET'], strict_slashes=False)
def retrieve_state_route(state_id):
    """This endpoint retrives a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state_route(state_id):
    """This endpoint deletes a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state_route():
    """This endpoint creates a state object"""
    state_data = request.get_json()
    if state_data is None:
        abort(400, 'Not a JSON')

    if 'name' not in state_data:
        abort(400, 'Missing name')
    state = State(**state_data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_route(state_id):
    """This endpoint updates a state object"""
    state_data = request.json
    if state_data is None:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in state_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
