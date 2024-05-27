#!/usr/bin/python3
"""This contains all API endpoints"""
from api.v1.views import app_views
from models import storage

from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status_route():
    """This endpoint returns the status of the API"""
    return jsonify({"staus": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats_route():
    """This endpoint retrieves the number of each objects by type"""
    return storage.count()
