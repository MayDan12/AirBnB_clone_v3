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

@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Route: /stats
    Method: GET
    Description: Returns a JSON representation of the
    number of each object type in the storage.
    """
    from models import storage
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.place import Place
    from models.review import Review
    from models.user import User

    return jsonify({
        "states": storage.count(State),
        "cities": storage.count(City),
        "amenities": storage.count(Amenity),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "users": storage.count(User)
    })
