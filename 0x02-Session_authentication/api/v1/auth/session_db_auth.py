#!/usr/bin/env python3
'''
This module contains the SessionDBAuth class
'''

from .session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from os import getenv
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    '''
    SessionDBAuth class

    Args:
        SessionExpAuth: inherits from SessionExpAuth

    Methods:
        create_session
        user_id_for_session_id
        destroy_session'''

    def __init__(self) -> None:
        '''
        Constructor
        Args:
            self: instance of the class

        Returns:
            None
        '''
        super().__init__()
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
        kws = {"user_id": user_id, "session_id": sess_id}
        UsrSess = UserSession(**kws)
        UsrSess.save()
        UsrSess.save_to_file()
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        '''
        returns a User ID based on a Session ID
        Args:
            session_id: the Session ID
        Returns:
            str: the User ID
        '''
        if not session_id:
            return None

        UserSession.load_from_file()
        userSesh = UserSession.search({'session_id': session_id})

        if not userSesh:
            return None

        usR = userSesh[0]

        expTime = (usR.created_at + timedelta(seconds=self.session_duration))

        if expTime < datetime.utcnow():
            return None

        return usR.user_id

    def destroy_session(self, request=None):
        '''
        deletes the user session / logout
        Args:
            request: the request
        Returns:
            bool: True if the session was deleted, False otherwise
        '''
        if not request:
            return False
        sess_id = self.session_cookie(request)
        if not sess_id:
            return False
        usrId = self.user_id_for_session_id(sess_id)
        if not usrId:
            return False
        usrSess = UserSession.search({"session_id": sess_id})
        if usrSess:
            usrSess[0].remove()
            UserSession.save_to_file()
            return True
        return False
