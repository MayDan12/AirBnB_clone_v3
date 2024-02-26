#!/usr/bin/python3
"""This is the route for handling Place objects and operations"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places_by_city(city_id):
    """
    retrieves all Place objects by city
    """
    place_list = []
    city_obj = storage.get("City", str(city_id))
    for obj in city_obj.places:
        place_list.append(obj.to_dict())

    return jsonify(place_list)