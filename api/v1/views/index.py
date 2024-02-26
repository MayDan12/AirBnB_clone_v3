#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """
    Route: /status
    Method: GET
    Description: Returns a JSON representation of the status of the API.
    """
    return jsonify({"status": "OK"})
