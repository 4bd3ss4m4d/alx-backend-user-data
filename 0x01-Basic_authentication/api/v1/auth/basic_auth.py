#!/usr/bin/env python3
""" Module of basic auth views
"""
from .auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic User Auth"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Basic - Base64 part
         returns the Base64 part of the Authorization header
         for a Basic Authentication"""
        if (authorization_header is None or
            type(authorization_header) is not str or
                not authorization_header.startswith("Basic ")):
            # print(authorization_header)
            return None
        return (authorization_header[6:])

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns the decoded value of a base64 string"""
        if (base64_authorization_header is None or
                type(base64_authorization_header) is not str):
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode()
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """returns user email and password from the Base64 decoded value
        """
        if (decoded_base64_authorization_header is None or
            type(decoded_base64_authorization_header) is not str or
                ":" not in decoded_base64_authorization_header):
            return None, None
        return decoded_base64_authorization_header.split(':', 1)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Basic - User object"""
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
        """ overloads Auth and retrieves the
            User instance for a request
        """
        raw_header = self.authorization_header(request)
        to_b64 = self.extract_base64_authorization_header(raw_header)
        decoded = self.decode_base64_authorization_header(to_b64)
        clean_data = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(*clean_data)
