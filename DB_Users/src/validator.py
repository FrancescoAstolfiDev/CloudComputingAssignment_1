import re
from typing import Optional

from pydantic import ValidationError, EmailStr

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

    def insert_user(self, user:UserInDB) ->Optional[UserInDB]:
        """
        Try to convert the dict in input to a UserInDB.
        Raises ValueError if the conversion is not possible.
        """
        # Insert the validated user into the database
        user=self.manager.create_user(user)
        if user is None:
            raise ValueError("Invalid user ID or password")
        return user

    def get_user_by_userid(self, user_id: str) -> UserInDB:
        """Get user by user_id"""
        user = self.manager.get_user(user_id)
        if user is None:
            raise ValueError("Invalid user ID or password")
        return user

    def get_user_by_email(self, email: str) -> UserInDB:
        """Get user by email"""
        user = self.manager.get_user_by_email(email)
        if user is None:
            raise ValueError("Invalid user ID or password")
        return user

    def get_user(self, identifier: str) -> UserInDB:
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


if __name__ == "__main__":
    service = UserValidator.get_instance()
    user_data = {
        "_id": "1234598",
        "email": "test@example.com",  # added email
        "params": {
            "humor": 3,
            "empathy": 4,
            "optimism": 2
        },
        "hashed_password": "$2b$12$ge8TS7zhIrfgrBcDASfBn.q/QBv18CzCenvAMBDtITdfBJj.nils.",
        "created_at": {
            "$date": "2025-09-20T08:58:29.074Z"
        }
    }
    service.insert_user(user_data)
