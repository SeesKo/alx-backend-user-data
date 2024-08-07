#!/usr/bin/env python3
"""
UserSession model for storing sessions in a database
"""
from models.base import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class UserSession(Base):
    """ UserSession class to store session data """
    
    __tablename__ = 'user_sessions'
    
    user_id = Column(String(60), nullable=False)
    session_id = Column(String(60), primary_key=True, nullable=False)
    
    def __init__(self, *args, **kwargs):
        """ Initialize a UserSession instance """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
