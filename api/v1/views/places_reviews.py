#!/usr/bin/python3
"""
route for handling Review objects and operations
"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views, storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def reviews_by_place(place_id):
    """
    retrieves all Review objects by place
    """
    place_obj = storage.get(Place, str(place_id))

    if place_obj is None:
        abort(404)

    reviews = [review.to_dict() for review in place_obj.reviews]
    return jsonify(reviews)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def review_create(place_id):
    """
    create REview route
    """
    place = storage.get(Place, place_id)
    if not place:
      abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')

    user_id = data.get('user_id')
    if not user_id:
        abort(400, 'Missing user_id')

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    text = data.get('text')
    if not text:
        abort(400, 'Missing text')

    new_review = Review(user_id=user_id, place_id=place_id, text=text)
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>",  methods=["GET"],
                 strict_slashes=False)
def review_by_id(review_id):
    """
    gets a specific Review object by ID
    """

    fetched_obj = storage.get(Review, review_id)

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_dict())


@app_views.route("/reviews/<review_id>",  methods=["PUT"],
                 strict_slashes=False)
def review_put(review_id):
    """
    updates specific Review object by ID
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    place_json = request.get_json(silent=True)

    if place_json is None:
        abort(400, 'Not a JSON')

    for key, value in place_json.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200


@app_views.route("/reviews/<review_id>",  methods=["DELETE"],
                 strict_slashes=False)
def review_delete_by_id(review_id):
    """
    deletes Review by id
    """

    fetched_obj = storage.get(Review, str(review_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({}), 200
