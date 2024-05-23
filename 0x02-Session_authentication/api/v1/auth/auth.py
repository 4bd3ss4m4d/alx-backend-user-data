#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from typing import TypeVar, List
from os import getenv


class Auth:
    '''
    Auth class
    Methods:
        require_auth
        authorization_header
        current_user
        session_cookie
    '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False"""
        if not path or not excluded_paths or excluded_paths == []:
            return True

        if not path.endswith('/'):
            path = path + '/'

        for xclude in excluded_paths:
            if xclude == path or path.startswith(xclude.split('*')[0]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None"""
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request
        """
        if request is None:
            return None
        _my_session_id = getenv("SESSION_NAME")
        return request.cookies.get(_my_session_id)
