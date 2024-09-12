#!/usr/bin/env python3
"""DB module for user authentication service"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Dict, Any

from user import Base, User


class DB:
    """DB class for handling database operations"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database
        
        Args:
            email (str): The email of the user
            hashed_password (str): The hashed password of the user
        
        Returns:
            User: The newly created User object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs: Dict[str, Any]) -> User:
        """
        Find a user in the database based on input arguments
        
        Args:
            **kwargs: Arbitrary keyword arguments for filtering
        
        Returns:
            User: The found User object
        
        Raises:
            NoResultFound: If no user is found
            InvalidRequestError: If invalid arguments are provided
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs: Dict[str, Any]) -> None:
        """
        Update user attributes
        
        Args:
            user_id (int): The ID of the user to update
            **kwargs: Arbitrary keyword arguments for updating user attributes
        
        Raises:
            ValueError: If an invalid attribute is provided
            NoResultFound: If no user is found with the given ID
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError
            self._session.commit()
        except NoResultFound:
            raise NoResultFound
