from pydantic import BaseModel, Field, EmailStr, field_validator
from .userparams import UserParams

class UserResponse(BaseModel):
    user_id: str
    params: UserParams = Field(..., description="Param of the user")

    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v):
        """Verify the len of the user_id 7 char len """
        if len(v) != 7:
            raise ValueError("user_id not valid ")
        return v

class UserCreate(BaseModel):
    password: str
    email: EmailStr



class LoginRequest(BaseModel):
    identifier: str  # può essere user_id o email
    password: str


class UserFullResponse(UserResponse):
    """Model that rapresent the data in the mongoDB"""
    email:EmailStr=Field(...,  description="email of the user")
    hashed_password: str = Field(..., description="crypted password")