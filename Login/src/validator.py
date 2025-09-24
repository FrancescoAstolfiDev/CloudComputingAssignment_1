import re
from typing import Optional, Any

from  .manager import UserManager
from  .schemas import UserCreate, UserResponse
from .model import UserInDB
from  .userparams import UserParams


class UserValidator:
    _instance = None  # singleton instance
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserValidator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
       self.manager=UserManager.get_instance()

    @classmethod
    def get_instance(cls):
        """return the singleton instance of the class"""
        if cls._instance is None:
            cls._instance = UserValidator()
        return cls._instance

    def password_validator(self,password):
        # Password validation
        if len(password) < 8:
            raise ValueError("The password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            raise ValueError("The password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            raise ValueError("The password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', password):
            raise ValueError("The password must contain at least one number")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            raise ValueError("The password must contain at least one special character")
        return 0


    def create_user(self, user: UserInDB)->Optional[UserInDB]:
        """Create a new user in the database"""
        # Password validation
        try :
            self.password_validator(user.password)
        except ValueError:
            raise ValueError
        # If everything is valid, create the user
        user=UserInDB(user_id="0000000", email=user.email, hashed_password=user.password, params=UserParams())
        user=self.manager.create_user(user)
        return user

    def out_user(self, dict: Any)->Optional[UserResponse]:
        return UserResponse(
            user_id=dict["user_id"],
            params=UserParams(**dict["params"])
        )

    def matching_pswd(self, password_input: str, password_found: str) -> bool:
        """log of the user and check of the matching password"""
        try:
            self.password_validator(password_input)
        except ValueError:
            raise ValueError
        print("prima della verifica delle password")
        print(self.manager.matching_pswd(password_input, password_found))
        if not self.manager.matching_pswd(password_input, password_found):
            raise ValueError("Invalid credentials")
        return True


