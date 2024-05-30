#!/usr/bin/env python3

'''
This module contains the main code for the API
'''

from flask import Flask, abort, jsonify, request, redirect, url_for
from auth import Auth

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
AUTH = Auth()


@app.route("/")
def home() -> str:
    '''
    This function returns a welcome message
    Returns:
        str: Welcome message
    '''
    return jsonify({"message": "Bienvenue"})


@app.route("/sessions", methods=["POST"])
def login():
    '''
    This function logs in a user
    Returns:
        str: JSON representation of the user email and a message
    '''
    mail = request.form.get("email")
    psswd = request.form.get("password")
    if not AUTH.valid_login(mail, psswd):
        abort(401)
    sessId = AUTH.create_session(mail)
    resp = jsonify({"email": mail, "message": "logged in"})
    resp.set_cookie("session_id", sessId)
    return resp


@app.route("/sessions", methods=["DELETE"])
def logout():
    '''
    This function logs out a user
    Returns:
        str: Redirects to the home page
    '''
    sessId = request.cookies.get("session_id")
    usr = AUTH.get_user_from_session_id(sessId)
    if not usr:
        abort(403)
    AUTH.destroy_session(usr.id)
    return redirect(url_for("home"))


@app.route("/users", methods=["POST"])
def users():
    '''
    This function registers a user
    '''
    mail = request.form.get("email")
    passwd = request.form.get("password")
    try:
        AUTH.register_user(mail, passwd)
        return jsonify({"email": mail, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/profile")
def profile() -> str:
    """ User profile endpoint
        Return:
            - user email JSON represented
            - 403 if session_id is not linked to any user
    """
    sessID = request.cookies.get("session_id")
    usr = AUTH.get_user_from_session_id(sessID)
    if not usr:
        abort(403)
    return jsonify({"email": usr.email})


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    '''
    This function generates a reset password token
    Returns:
        str: JSON representation of the user email and the reset token
    '''
    eml = request.form.get("email")
    try:
        resTkn = AUTH.get_reset_password_token(eml)
    except ValueError:
        abort(403)

    return jsonify({"email": eml, "reset_token": resTkn})


@app.route("/reset_password", methods=["PUT"])
def update_password():
    '''
    This function updates the user password
    Returns:
        str: JSON representation of the user email and a message
    '''
    eml = request.form.get("email")
    newPswd = request.form.get("new_password")
    resTkn = request.form.get("reset_token")

    try:
        AUTH.update_password(resTkn, newPswd)
    except ValueError:
        abort(403)
    return jsonify({"email": eml, "message": "Password updated"})


if __name__ == "__main__":
