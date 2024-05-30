#!/usr/bin/env python3

'''
This module contains the main code for the API
'''

import bcrypt
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from db import DB


class Auth:
    '''
    This class is responsible for user authentication
    Attributes:
        - _db: DB instance
    Methods:
        - register_user: Registers new user
        - valid_login: Checks if password is valid
        - create_session: Creates session for user
        - get_user_from_session_id: Gets user based on their session id
        - destroy_session: Destroys user session
        - get_reset_password_token: Generates reset password token for valid user
        - update_password: Update password for user with matching reset token
    '''

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
        Registers new user
        Args:
            - email: user's email
            - password: user's password
        Return:
            - User instance
        '''
        db = self._db
        try:
            usr = db.find_user_by(email=email)
        except NoResultFound:
            usr = db.add_user(email, _hash_password(password))
            return usr
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        '''
        Checks if password is valid
        Args:
            - email: user's email
            - password: user's password
        Return:
            - True if password is valid else False
        '''
        db = self._db
        try:
            usr = db.find_user_by(email=email)
        except NoResultFound:
            return False
        if not bcrypt.checkpw(password.encode('utf-8'), usr.hashed_password):
            return False
        return True

    def create_session(self, email: str) -> str:
        '''
        Creates session for user
        Args:
            - email: user's email
        Return:
            - session_id
        '''
        db = self._db
        try:
            usr = db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        db.update_user(usr.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        '''
        Gets user based on their session id
        Args:
            - session_id: user's session id
        Return:
            - User instance
        '''
        if not session_id:
            return None
        db = self._db
        try:
            user = db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        '''
        Destroys user session
        Args:
            - user_id: user's id
        Return:
            - None'''
        db = self._db
        db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        '''
        Generates reset password token for valid user
        Args:
            - email: user's email
        Return:
            - reset_token
        '''
        db = self._db
        try:
            usr = db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        resTkn = _generate_uuid()
        db.update_user(usr.id, reset_token=resTkn)
        return resTkn

    def update_password(self, reset_token: str, password: str) -> None:
        '''
        Update password for user with matching reset token
        Args:
            - reset_token: user's reset token
            - password: user's new password
        Return:
            - None
        '''
        db = self._db
        try:
            usr = db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        db.update_user(usr.id, hashed_password=_hash_password(password),
                       reset_token=None)


def _hash_password(password: str) -> bytes:
    '''
    Hashes password
    Args:
        - password: user's password
    Return:
        - hashed password
    '''
    encodedPswd = password.encode()
    return bcrypt.hashpw(encodedPswd, bcrypt.gensalt())


def _generate_uuid() -> str:
    '''
    Generates a random UUID
    Return:
        - str: UUID
    '''
    return str(uuid4())
