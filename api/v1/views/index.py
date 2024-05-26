#!/usr/bin/python3
"""This contains all API endpoints"""
from api.v1.views import app_views

from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status_route():
    """This endpoint returns the status of the API"""
    return jsonify({"staus": "OK"})
