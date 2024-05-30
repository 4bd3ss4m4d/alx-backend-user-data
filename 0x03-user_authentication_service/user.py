#!/usr/bin/env python3

'''
This is the main file for the flask app
'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    '''
    User class
    
    Attributes:
        id: int: User ID
        email: str: User email
        hashed_password: str: User hashed password
        session_id: str: User session ID
        reset_token: str: User reset token
    '''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
