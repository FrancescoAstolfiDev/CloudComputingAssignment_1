import re
from typing import Optional

from pydantic import ValidationError, EmailStr

from .schemas import UserNoAlias,UserUpdate
from .manager import UserManager
from .model import UserInDB

class UserValidator:
    _instance = None  # singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserValidator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.manager = UserManager.get_instance()

    @classmethod
    def get_instance(cls):
        """Return the singleton instance of the class"""
        if cls._instance is None:
            cls._instance = UserValidator()
        return cls._instance
    def inner_convertion(self,user:UserInDB)->UserNoAlias:
        return UserNoAlias(
            user_id=user.user_id,
            params=user.params,
            hashed_password=user.hashed_password,
            email=user.email
        )
    def insert_user(self, user:UserNoAlias) ->Optional[UserNoAlias]:
        """
        Try to convert the dict in input to a UserInDB.
        Raises ValueError if the conversion is not possible.
        """
        # Insert the validated user into the database
        user=UserInDB(_id=user.user_id, email=user.email, hashed_password=user.hashed_password, params=user.params)
        user=self.manager.insert_user(user)
        if user is None:
            raise ValueError("Invalid user ID or password")
        return self.inner_convertion(user)

    def edit_user(self, user:UserUpdate) -> int :
        edit=self.manager.edit_user(user)
        print("return from validator")
        return edit

    def get_user_by_userid(self, user_id: str) -> UserNoAlias:
        """Get user by user_id"""
        user = self.manager.get_user(user_id)
        if user is None:
            raise ValueError("Invalid user ID or password")
        return self.inner_convertion(user)

    def get_user_by_email(self, email: str) -> UserNoAlias:
        """Get user by email"""
        user = self.manager.get_user_by_email(email)
        if user is None:
            raise ValueError("Invalid user ID or password")
        return self.inner_convertion(user)

    def get_user(self, identifier: str) ->UserNoAlias:
        """
        Unified get_user function:
        - if identifier is email → get_user_by_email
        - if identifier is user_id (7 chars) → get_user_by_userid
        """
        # Check if it's a valid email
        if identifier.__contains__("@"):
             return self.get_user_by_email(identifier)


        # Check if it's a 7-character user_id
        if len(identifier) == 7:
            return self.get_user_by_userid(identifier)

        raise ValueError("Identifier must be either a valid email or a 7-character user ID")

