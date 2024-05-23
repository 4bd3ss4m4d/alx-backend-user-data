#!/usr/bin/env python3
""" Module of session auth views
"""
from models.user import User
from uuid import uuid4
from .auth import Auth
from typing import TypeVar


class SessionAuth(Auth):
    """Basic User Auth"""

    usrIdBySessionId = {}

    def create_session(self, user_id: str = None) -> str:
        '''
        instance method that creates a Session ID for a user_id
        Returns:
            str: the Session ID
        '''
        if user_id is None or not isinstance(user_id, str):
            return None

        sess_Id = str(uuid4())
        # subscript Notatation
        self.usrIdBySessionId[sess_Id] = user_id
        return sess_Id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
        instance method that returns a User ID based on a Session ID
        Returns:
            str: the User ID
        '''
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.usrIdBySessionId.get(session_id)

    def current_user(self, request=None):
        '''
        instance method that returns a User instance based on a cookie value
        Returns:
            User: the User instance
        '''
        sess_id = self.session_cookie(request)
        usr_id = self.user_id_for_session_id(sess_id)
        return User.get(usr_id)

    def destroy_session(self, request=None):
        '''
        instance method that deletes the user session / logout
        Returns:
            bool: True if the session was deleted, False otherwise
        '''
        if not request:
            return False
        sess_id = self.session_cookie(request)
        if not sess_id or not self.user_id_for_session_id(sess_id):
            return False
        self.usrIdBySessionId.pop(sess_id)
        return True
