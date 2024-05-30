#!/usr/bin/env python3

'''
This is the main file for the flask app
'''

from bcrypt import hashpw, gensalt, checkpw
from user import User
from sqlalchemy.orm.exc import NoResultFound
from db import DB


def _hash_password(password: str) -> bytes:
    '''
    Hashes a password
    Args:
        password: str: Password to hash
    Returns:
        bytes: Hashed password
    '''
    return hashpw(password.encode('utf-8'), gensalt())


class Auth:
    '''
    Auth class
    
    Methods:
        register_user: Registers a new user
        valid_login: Checks if a login is valid
    '''
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
        Register a new user
        Args:
            email: str: Email of user
            password: str: Password of user
        Returns:
            User: New user
        '''
        try:
            exists = self._db.find_user_by(email=email)
            if exists:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            nuser = self._db.add_user(email, _hash_password(password))
            return nuser

    def valid_login(self, email: str, password: str) -> bool:
        '''
        Validates a login
        Args:
            email: str: Email of user
            password: str: Password of user
        Returns:
            bool: True if login is valid, False otherwise
        '''
        try:
            usr = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), usr.hashed_password)
        except NoResultFound:
            return False
