import random
from typing import Optional

from passlib.context import CryptContext
from .model import UserInDB
from .userparams import UserParams

class UserManager:
    """Handle the user database operations"""

    _instance = None  # singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # ensure that the instance is initialized only once
        if not hasattr(self, "pwd_context"):
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            self.pwd_context = pwd_context
        self.db_name="users"

    @classmethod
    def get_instance(cls):
        """return the singleton instance of the class"""
        if cls._instance is None:
            cls._instance = UserManager()
        return cls._instance


    def uid_generator(self)-> str:
        return ''.join(str(random.randint(0, 9)) for _ in range(7))

    def create_user(self, user: UserInDB)->Optional[UserInDB]:
        """create a new user in the database"""
        user_dict = user.model_dump(by_alias=True)
        hashed_password = self.pwd_context.hash(user.hashed_password)
        user_dict["hashed_password"] = hashed_password
        user_dict["user_id"] = self.uid_generator()
        user_dict["params"] = UserParams()
        return UserInDB(**user_dict)




    def matching_pswd(self, password_input: str, password_found: str )-> bool:
        """log of the user and check of the matching password"""
        return self.pwd_context.verify(password_input, password_found)


