#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from user import Base, User


class DB:
    '''
    DB class
    
    Methods:
        add_user: Add a new user
        find_user_by: Find a user by a given attribute
        update_user: Update a user by a given attribute
    '''

    def __init__(self) -> None:
        '''
        Constructor
        
        Returns:
            None
        '''
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        '''
        Session property
        
        Returns:
            Session: Session object
        '''
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''
        Add a new user
        Args:
            email: str: Email of user
            hashed_password: str: Hashed password of user
        Returns:
            User: New user
        '''
        nuser = User(email=email, hashed_password=hashed_password)
        self._session.add(nuser)
        self._session.commit()
        return nuser

    def find_user_by(self, **kwargs) -> User:
        '''
        Find a user by a given attribute
        Args:
            **kwargs: Arbitrary keyword arguments
        Returns:
            User: User object
        '''
        try:
            usr = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        return usr

    def update_user(self, user_id: int, **kwargs) -> None:
        '''
        Update a user by a given attribute
        Args:
            user_id: int: User id
            **kwargs: Arbitrary keyword arguments
        Returns:
            None
        '''
        usr = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if not hasattr(User, k):
                raise ValueError()
            setattr(usr, k, v)
        return None
