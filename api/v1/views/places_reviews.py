#!/usr/bin/python3

""" Configures RESTful api for the places_reviews route """
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """This methods retrieves the list of all reviews"""
    review_list = []
    review_obj = storage.get("Place", str(place_id))

    if review_obj is None:
        abort(404)

    for obj in review_obj.reviews:
        review_list.append(obj.to_dict())

    return jsonify(review_list)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_reviews(place_id):
    """This methods creates a new review obj"""
    review_json = request.json
    if review_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", place_id):
        abort(404)
    if not storage.get("User", review_json["user_id"]):
        abort(404)
    if "user_id" not in review_json:
        abort(400, 'Missing user_id')
    if "text" not in review_json:
        abort(400, 'Missing text')

    review_json['place_id'] = place_id

    review_new = Review(**review_json)
    review_new.save()
    response = jsonify(review_new.to_dict())
    response.status_code = 201

    return response


@app_views.route("/reviews/<review_id>",  methods=["GET"],
                 strict_slashes=False)
def review_byid(review_id):
    """
    This method gets a specific Review object by ID
    """

    fetch_obj = storage.get("Review", str(review_id))

    if fetch_obj is None:
        abort(404)

    return jsonify(fetch_obj.to_dict())

@app_views.route("/reviews/<review_id>",  methods=["PUT"],
                 strict_slashes=False)
def review_put(review_id):
    """
    This method updates specific Review object by ID
    """
    place_json = request.json

    if place_json is None:
        abort(400, 'Not a JSON')

    fetch_obj = storage.get("Review", str(review_id))

    if fetch_obj is None:
        abort(404)

    for key, value in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id",
                       "place_id"]:
            setattr(fetch_obj, key, value)

    fetch_obj.save()

    return jsonify(fetch_obj.to_dict())


@app_views.route("/reviews/<review_id>",  methods=["DELETE"],
                 strict_slashes=False)
def review_delete_by_id(review_id):
    """
    This method deletes Review by id
    """

    fetched_obj = storage.get("Review", str(review_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})
