#!/usr/bin/env python3
""" Module of basic auth views
"""
from .auth import Auth
from typing import TypeVar
from models.user import User
import base64


class BasicAuth(Auth):
    '''
    Basic Auth class
    Args:
        Auth: inherits from Auth
    Methods:
        extract_base64_authorization_header
        decode_base64_authorization_header
        extract_user_credentials
        user_object_from_credentials
        current_user
    '''

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        '''
        returns the Base64 part of the Authorization header for a Basic
        Returns:
            str: the Base64 part of the Authorization header
        '''
        if (authorization_header is None or
            type(authorization_header) is not str or
                not authorization_header.startswith("Basic ")):
            # print(authorization_header)
            return None
        return (authorization_header[6:])

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''
        returns the decoded value of a Base64 string
        Returns:
            str: the decoded value of a Base64 string
        '''
        if (base64_authorization_header is None or
                type(base64_authorization_header) is not str):
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode()
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''
        returns the user email and password from the Base64 decoded value
        Returns:
            tuple: the user email and password from the Base64 decoded value
        '''
        if (decoded_base64_authorization_header is None or
            type(decoded_base64_authorization_header) is not str or
                ":" not in decoded_base64_authorization_header):
            return None, None
        return decoded_base64_authorization_header.split(':', 1)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''
        returns the User instance based on his email and password
        Returns:
            User: the User instance based on his email and password
        '''
        if (user_email is None or
            type(user_email) is not str or
                type(user_pwd) is not str):
            return None
        if (User.search({'email': user_email})):
            users = User.search({'email': user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
                return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        overloads Auth and retrieves the User instance for a request
        Returns:
            User: the User instance for a request
        '''
        rw_hdt = self.authorization_header(request)
        b64 = self.extract_base64_authorization_header(rw_hdt)
        dcdd = self.decode_base64_authorization_header(b64)
        cleaned = self.extract_user_credentials(dcdd)
        return self.user_object_from_credentials(*cleaned)
