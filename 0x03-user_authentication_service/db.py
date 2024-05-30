#!/usr/bin/env python3

'''
This module contains the main code for the API
'''

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError



class DB:
    '''
    This class is responsible for database operations
    Attributes:
        - _engine: Engine instance
        - __session: Session instance
    Methods:
        - add_user: Adds new user to the database
        - find_user_by: Finds user by a given attribute
        - update_user: Updates user instance
    '''

    def __init__(self) -> None:
        '''
        Initializes the DB class
        '''
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        '''
        Returns the current session
        Return:
            - Session instance
        '''
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''
        Adds new user to the database
        Args:
            - email: user's email
            - hashed_password: user's hashed password
        Return:
            - User instance'''
        sess = self._session
        try:
            nUser = User(email=email, hashed_password=hashed_password)
            sess.add(nUser)
            sess.commit()
        except Exception:
            sess.rollback()
            nUser = None
        return nUser

    def find_user_by(self, **kwargs) -> User:
        '''
        Finds user by a given attribute
        Args:
            - **kwargs: Arbitrary keyword arguments
        Return:
            - User instance or raises NoResultFound exception
        '''
        ats, values = [], []
        for attr, val in kwargs.items():
            if not hasattr(User, attr):
                raise InvalidRequestError()
            ats.append(getattr(User, attr))
            values.append(val)

        session = self._session
        que = session.query(User)
        usR = que.filter(tuple_(*ats).in_([tuple(values)])).first()
        if not usR:
            raise NoResultFound()
        return usR

    def update_user(self, user_id: int, **kwargs) -> None:
        '''
        Updates user instance
        Args:
            - user_id: user's id
            - **kwargs: Arbitrary keyword arguments
        Return:
            - None
        '''
        usR = self.find_user_by(id=user_id)
        session = self._session
        for attribute, value in kwargs.items():
            if not hasattr(User, attribute):
                raise ValueError
            setattr(usR, attribute, value)
        session.commit()
