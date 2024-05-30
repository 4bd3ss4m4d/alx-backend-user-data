#!/usr/bin/env python3

'''
This is the main file for the flask app
'''

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route('/')
def index():
    '''
    Index route
    Returns:
        dict: Welcome message
    '''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    '''
    Users route
    Returns:
        dict: User created message
    '''
    ml = request.form.get('email')
    pswd = request.form.get('password')
    if ml and pswd:
        try:
            AUTH.register_user(ml, pswd)
            return jsonify({"email": ml, "message": "user created"})
        except ValueError:
            return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({"message": "email and password is required"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
