#!/usr/bin/env python3
'''
This module contains the SessionExpAuth class
'''

from os import getenv
from .session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    '''
    SessionExpAuth class

    Args:
        SessionAuth: inherits from SessionAuth

    Methods:
        create_session
        user_id_for_session_id
    '''

    def __init__(self) -> None:
        '''
        Constructor
        Args:
            self: instance of the class'''
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        '''
        creates a session ID for a user_id
        Args:
            user_id: the user ID
        Returns:
            str: the session ID
        '''
        sess_id = super().create_session(user_id)
        if not sess_id:
            return None
        session_dictionary = {}
        session_dictionary['user_id'] = user_id
        session_dictionary['created_at'] = datetime.now()

        self.usrIdBySessionId[sess_id] = session_dictionary
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        '''
        returns a User ID based on a Session ID
        Args:
            session_id: the Session ID
        Returns:
            str: the User ID
        '''
        if not session_id or not self.usrIdBySessionId.get(session_id):
            return None

        sessDit = self.usrIdBySessionId.get(session_id)
        if not sessDit:
            return None

        if self.session_duration <= 0:
            return sessDit.get("user_id")

        if not sessDit.get("created_at"):
            return None
        ex_isec = timedelta(seconds=self.session_duration)
        if (ex_isec + sessDit.get("created_at") < datetime.now()):
            return None
        return sessDit.get("user_id")
