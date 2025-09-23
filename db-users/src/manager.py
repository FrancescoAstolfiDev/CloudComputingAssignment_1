from typing import Optional
from passlib.context import CryptContext
from .model import UserInDB
from .schemas import UserUpdate
from .database import db_manager


class UserManager:
    """Singleton manager for user database operations (Database Service)"""

    _instance = None  # singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # ensure that the instance is initialized only once
        if not hasattr(self, "pwd_context"):
            self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.db_name = "users"

    @classmethod
    def get_instance(cls) :
        """Return the singleton instance of the class"""
        if cls._instance is None:
            cls._instance = UserManager()
        return cls._instance

    def unique_email(self, email: str) -> bool:
        """Verify that the email is unique in the database"""
        user_from_db = db_manager.find_one(self.db_name, {"email": email})
        return user_from_db is None

    def insert_user(self, user: UserInDB)-> Optional[UserInDB]:
        """Insert a new user into the database"""
        if(not self.unique_email(user.email)):
          return None
        user_dict = user.model_dump(by_alias=True)
        db_manager.insert_document(self.db_name, user_dict)
        return user

    def edit_user(self, user: UserUpdate)-> int :
        """Edit an existing user in the database"""
        val=db_manager.update_document(self.db_name, {"_id": user.user_id}, { "params": user.params.to_dict()})
        print("return from manager")
        return val


    def get_user(self, user_id: str) -> Optional[UserInDB]:
        """Return the user from the database, or None if not found"""
        user_from_db = db_manager.find_one(self.db_name, {"_id": user_id})
        if not user_from_db:
            return None
        # Convert dictionary from DB back into UserInDB instance
        return UserInDB.model_validate(user_from_db)

    def get_user_by_email(self,email:str) -> Optional[UserInDB]:
        user_from_db = db_manager.find_one(self.db_name, {"email":email})
        if not user_from_db:
            return None
        # Convert dictionary from DB back into UserInDB instance
        return UserInDB.model_validate(user_from_db)
