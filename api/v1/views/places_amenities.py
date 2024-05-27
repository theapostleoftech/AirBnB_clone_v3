#!/usr/bin/python3
"""This holds the views for place amenities"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv

current_storage = getenv("HBNB_TYPE_STORAGE")


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=['GET'])
def retrieve_amenity_places_route(place_id):
    """This endpoint lists all amenities in a place"""
    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity_place_route(place_id, amenity_id):
    """This endpoint deletes an amenity object"""
    place = storage.get(Place, place_id)
    if place:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            if current_storage != "db":
                if amenity.id not in place.amenity_ids:
                    abort(404)
                place.amenity_ids.remove(amenity.id)
            else:
                if amenity not in place.amenities:
                    abort(404)
                place.amenities.remove(amenity)
            storage.save()
            return jsonify({}), 200
        abort(404)
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['POST'])
def create_amenity_place_route(place_id, amenity_id):
    """This endpoint creates an amenity for a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if current_storage != "db":
        if amenity.id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity.id)
        storage.save()
        return jsonify(amenity.to_dict()), 201
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
