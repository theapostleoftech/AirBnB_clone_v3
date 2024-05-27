#!/usr/bin/python3
"""This holds views for the place reviews"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET'])
def retrieve_review_places_route(place_id):
    """This endpoint lists all reviews of a place"""
    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify([review.to_dict() for review in place.reviews])
    abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['GET'])
def retrieve_review_route(review_id):
    """This endpoint lists a review object"""
    review = storage.get(Review, review_id)
    if review is not None:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_review_route(review_id):
    """This endpoint deletes a review object"""
    review = storage.get(Review, review_id)
    if review is not None:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['POST'])
def update_review_route(place_id):
    """This endpoint creates a review of a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_data = request.get_json()
    if not review_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in review_data:
        abort(400, 'Missing user_id')
    user_id = request.get_json()["user_id"]
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'text' not in review_data:
        abort(400, 'Missing text')
    new_review = Review(**review_data())
    new_review.place_id = place_id
    new_review.user_id = user.id
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['PUT'])
def update_review_route(review_id):
    """This endpoint updates the review object"""
    review_data = request.get_json()
    if not review_data:
        abort(400, 'Not a JSON')
    review = storage.get(Review, review_id)
    if review is not None:
        for attr, value in review_data().items():
            if (hasattr(review, attr) and
                    attr != 'id' and attr != 'created_at' and
                    attr != 'updated_at' and attr != 'user_id' and
                    attr != 'place_id'):
                setattr(review, attr, value)
        storage.save()
        return jsonify(review.to_dict()), 200
    abort(404)
