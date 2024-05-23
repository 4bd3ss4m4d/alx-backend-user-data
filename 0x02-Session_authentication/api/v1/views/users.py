#!/usr/bin/env python3
'''
This module contains the User views
'''
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Return:
      - list of all User objects JSON represented
    """
    allUsrs = [user.to_json() for user in User.all()]
    return jsonify(allUsrs)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """

    if user_id == "me" and request.current_user is None:
        abort(404)

    if user_id == "me" and request.current_user is not None:
        return jsonify(request.current_user.to_json())

    if user_id is None:
        abort(404)

    usR = User.get(user_id)
    if usR is None:
        abort(404)

    return jsonify(usR.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - empty JSON is the User has been correctly deleted
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    usR = User.get(user_id)
    if usR is None:
        abort(404)
    usR.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    JSON body:
      - email
      - password
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """
    rej = None
    msgError = None
    try:
        rej = request.get_json()
    except Exception as e:
        rej = None
    if rej is None:
        msgError = "Wrong format"
    if msgError is None and rej.get("email", "") == "":
        msgError = "email missing"
    if msgError is None and rej.get("password", "") == "":
        msgError = "password missing"
    if msgError is None:
        try:
            user = User()
            user.email = rej.get("email")
            user.password = rej.get("password")
            user.first_name = rej.get("first_name")
            user.last_name = rej.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            msgError = "Can't create User: {}".format(e)
    return jsonify({'error': msgError}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ PUT /api/v1/users/:id
    Path parameter:
      - User ID
    JSON body:
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    if user_id is None:
        abort(404)
    Usr = User.get(user_id)
    if Usr is None:
        abort(404)
    rejj = None
    try:
        rejj = request.get_json()
    except Exception as e:
        rejj = None
    if rejj is None:
        return jsonify({'error': "Wrong format"}), 400
    if rejj.get('first_name') is not None:
        Usr.first_name = rejj.get('first_name')
    if rejj.get('last_name') is not None:
        Usr.last_name = rejj.get('last_name')
    Usr.save()
    return jsonify(Usr.to_json()), 200
