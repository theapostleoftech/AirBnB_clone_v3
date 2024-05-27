#!/usr/bin/python3
"""This holds views for the amenities objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False,
                 methods=['GET'])
def amenities_route():
    """This lists all the amenities objects"""
    return jsonify([amenity.to_dict() for amenity in storage.all(Amenity).values()])


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['GET'])
def get_amenity_id_route(amenity_id):
    """This ednpoint lists an amenity object"""
    amenity_by_id = storage.get(Amenity, amenity_id)
    if amenity_by_id is not None:
        return jsonify(amenity_by_id.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity_id_route(amenity_id):
    """This endpoint deletes the amenity object"""
    amenity_by_id = storage.get(Amenity, amenity_id)
    if amenity_by_id is not None:
        storage.delete(amenity_by_id)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/amenities", strict_slashes=False,
                 methods=['POST'])
def post_amenity_route():
    """This endpoint creates a new amenity object"""
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
def put_amenity_id_route(amenity_id):
    """This endpoint update an amenity object"""
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
