#!/usr/bin/env python3
"""
Session DB Auth for managing sessions stored in a database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class to manage sessions with database storage """

    def __init__(self):
        """ Initialize SessionDBAuth """
        super().__init__()
        self.engine = create_engine(getenv("DATABASE_URL"))
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def create_session(self, user_id=None):
        """ Create and store a new session ID """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        try:
            db_session = self.Session()
            user_session = UserSession(user_id=user_id, session_id=session_id)
            db_session.add(user_session)
            db_session.commit()
            return session_id
        except SQLAlchemyError:
            db_session.rollback()
            return None
        finally:
            db_session.close()

    def user_id_for_session_id(self, session_id=None):
        """ Get user ID by session ID from the database """
        if session_id is None:
            return None

        try:
            db_session = self.Session()
            user_session = (
                db_session.query(UserSession)
                .filter_by(session_id=session_id)
                .one_or_none()
            )
            if user_session is None:
                return None

            if self.session_duration > 0:
                if datetime.now() > (
                    user_session.created_at +
                    timedelta(seconds=self.session_duration)
                ):
                    return None

            return user_session.user_id
        except SQLAlchemyError:
            return None
        finally:
            db_session.close()

    def destroy_session(self, request=None):
        """ Destroy the session in the database """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        try:
            db_session = self.Session()
            user_session = (
                db_session.query(UserSession)
                .filter_by(session_id=session_id)
                .one_or_none()
            )
            if user_session is None:
                return False

            db_session.delete(user_session)
            db_session.commit()
            return True
        except SQLAlchemyError:
            db_session.rollback()
            return False
        finally:
            db_session.close()
