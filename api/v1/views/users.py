#!/usr/bin/python3

""" Configures RESTful api for the states route """
from flask import jsonify, request, abort
from api.v1.views import app_views, storage
from models import storage
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users(user_id):
  """This retrieves the list of all user objects"""
  user_list = []
  all_user =  storage.all(User)
  for obj in all_user.values():
    user_list.append(obj.to_dict())

  return jsonify(user_list)

@app_views.route('/users', methods=["POST"], strict_slashes=False)
def create_user():
  """
  create route for users
  Return the newly created user obj
  """
  user_json = request.get_json(silent=True)
  if user_json is None:
    abort(400, 'Not a JSON')
  if "email" not in user_json:
    abort(400, 'Missing email')
  if "password" not in user_json:
    abort(400, 'Missing password')

  new_user = User(**user_json)
  new_user.save()
  response = jsonify(new_user.to_dict())
  response.status_code = 201

  return response

@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def get_user_byid(user_id):
  """
  This gets a specific user object by id
  """

  fetch_obj = storage.get("User", str(user_id))

  if fetch_obj is None:
    abort(404)
  
  return jsonify(fetch_obj.to_dict())

@app_views.route('/users/<user_id>', methods=["PUT"], strict_slashes=False)
def put_user(user_id):
  """
  This updates specific user by id
  """
  user_json = request.get_json(silent=True)
  if user_json is None:
    abort(400,'Not a JSON')

  fetch_obj = storage.get("User", str(user_id))

  if fetch_obj is None:
    abort(404)

  for key, value in user_json.items():
    if key not in ["id", "created_at", "updated_at", "email"]:
      setattr(fetch_obj, key, value)

  fetch_obj.save()

  return jsonify(fetch_obj.to_dict())


@app_views.route('/users/<user_id>',  methods=["DELETE"], strict_slashes=False)
def delete_user_by_id(user_id):
    """
    This method deletes User by id
    """

    fetch_obj = storage.get("User", str(user_id))

    if fetch_obj is None:
        abort(404)

    storage.delete(fetch_obj)
    storage.save()

    return jsonify({})