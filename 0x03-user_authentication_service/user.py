#!/usr/bin/env python3

'''
This module contains the main code for the API
'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    '''
    This class represents a user
    Attributes:
        - id: User id
        - email: User email
        - hashed_password: User hashed password
        - session_id: User session id
        - reset_token: User reset token
    '''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
