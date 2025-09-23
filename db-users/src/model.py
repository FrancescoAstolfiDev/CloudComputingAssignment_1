from pydantic import BaseModel, Field, EmailStr
from .userparams import UserParams

class UserInDB(BaseModel):
    """Model that rapresent the data in the mongoDB"""
    user_id: str = Field(..., alias="_id", description="id of the user")
    email:EmailStr=Field(None,description="email of the user")
    hashed_password: str = Field(None,description="crypted password")
    params: UserParams = Field(..., description="params of the user")
    class Config:
        populate_by_name = True  # permette di usare sia user_id che _id