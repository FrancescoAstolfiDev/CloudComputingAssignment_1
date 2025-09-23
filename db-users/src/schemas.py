from pydantic import BaseModel, Field, EmailStr
from .userparams import UserParams
# suppose the data are already valdated
class UserNoAlias(BaseModel):
    """Model that rapresent the data in the mongoDB"""
    # after this response i dont want to see the _id
    user_id: str = Field(..., description="id of the user")
    email:EmailStr=Field(...,description="email of the user")
    hashed_password: str = Field(...,description="crypted password")
    params: UserParams = Field(..., description="params of the user")

class UserUpdate(BaseModel):
    """Model that rapresent the data in the mongoDB"""
    # after this response i dont want to see the _id
    user_id: str = Field(..., description="id of the user")
    params: UserParams = Field(..., description="params of the user")