#!/usr/bin/env python3

'''
This module contains the Auth class
'''

from api.v1.views import app_views
from typing import TypeVar, List
from flask import jsonify, abort, request


class Auth:
    '''
    Auth class

    Attributes:
        None

    Methods:
        require_auth(self, path: str, excluded_paths: List[str]) -> bool
        authorization_header(self, request=None) -> str
        current_user(self, request=None) -> TypeVar('User')
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
        This function checks if a path requires authentication

        Args:
            path: str
            excluded_paths: List[str]

        Returns:
            True if the path requires authentication, False otherwise
        '''
        if not path or not excluded_paths or excluded_paths == []:
            return True

        if not path.endswith('/'):
            path = path + '/'

        for nod_inc in excluded_paths:
            if nod_inc == path or path.startswith(nod_inc.split('*')[0]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        '''
        This function returns the value of the Authorization header

        Args:
            request: None

        Returns:
            The value of the Authorization header
        '''
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        This function returns the current user

        Args:
            request: None

        Returns:
            The current user
        '''
        return None
