from pydantic import BaseModel, Field, EmailStr
from .userparams import UserParams

class UserInDB(BaseModel):
    """Model that rapresent the data in the mongoDB"""
    user_id: str = Field(..., description="id of the user")
    email:EmailStr=Field(...,  description="email of the user")
    hashed_password: str = Field(..., description="crypted password")
    params: UserParams = Field(..., description="params of the user")
