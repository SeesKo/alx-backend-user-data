#!/usr/bin/env python3
"""
Module for UserSession model
"""
from models.base import Base


class UserSession(Base):
    """ UserSession model for storing sessions """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initializes a UserSession instance """
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        super().__init__(*args, **kwargs)

    @classmethod
    def create(cls, user_id, session_id):
        """ Create a new UserSession instance and save it """
        instance = cls(user_id=user_id, session_id=session_id)
        instance.save()
        return instance

    @classmethod
    def get(cls, session_id):
        """ Get a UserSession instance by session_id """
        instances = cls.search({'session_id': session_id})
        return instances[0] if instances else None

    @classmethod
    def delete(cls, session_id):
        """ Delete a UserSession instance by session_id """
        instance = cls.get(session_id)
        if instance:
            instance.remove()
