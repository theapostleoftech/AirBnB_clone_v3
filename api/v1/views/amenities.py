#!/usr/bin/python3
"""
    Manage the RESTfull API for amenities
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/amenities", strict_slashes=False,
                 methods=['GET'])
def amenities():
    """Display all the amenities"""
    return jsonify([ame.to_dict() for ame in storage.all(Amenity).values()])


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['GET'])
def get_amenity_id(amenity_id):
    """Display the amenity matched by id"""
    amenity_by_id = storage.get(Amenity, amenity_id)
    if amenity_by_id is not None:
        return jsonify(amenity_by_id.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity_id(amenity_id):
    """Delete the amenity matched by id"""
    amenity_by_id = storage.get(Amenity, amenity_id)
    if amenity_by_id is not None:
        storage.delete(amenity_by_id)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/amenities", strict_slashes=False,
                 methods=['POST'])
def post_amenity():
    """Create a new amenity"""
    json_req = request.get_json()
    if not json_req:
        abort(400, 'Not a JSON')
    if 'name' not in json_req:
        abort(400, 'Missing name')
    new_amenity = Amenity(**request.get_json())
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['PUT'])
def put_amenity_id(amenity_id):
    """Update a amenity in database"""
    json_req = request.get_json()
    if not json_req:
        abort(400, 'Not a JSON')
    amenity_by_id = storage.get(Amenity, amenity_id)
    if amenity_by_id is not None:
        for attr, value in request.get_json().items():
            if (hasattr(amenity_by_id, attr) and
                    attr != 'id' and attr != 'created_at' and
                    attr != 'updated_at'):
                setattr(amenity_by_id, attr, value)
        storage.save()
        return jsonify(amenity_by_id.to_dict()), 200
    abort(404)
