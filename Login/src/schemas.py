from pydantic import BaseModel, Field, EmailStr, field_validator
from .userparams import UserParams

class UserResponse(BaseModel):
    user_id: str
    params: UserParams = Field(..., description="Param of the user")

    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v):
        """Verifica che l'user_id sia lungo esattamente 7 caratteri"""
        if len(v) != 7:
            raise ValueError("user_id deve essere lungo esattamente 7 caratteri")
        return v

class UserCreate(BaseModel):
    password: str
    email: EmailStr



class LoginRequest(BaseModel):
    identifier: str  # può essere user_id o email
    password: str


class UserFullResponse(BaseModel):
    """Model that rapresent the data in the mongoDB"""
    user_id: str = Field(..., description="id of the user")
    email:EmailStr=Field(...,  description="email of the user")
    hashed_password: str = Field(..., description="crypted password")
    params: UserParams = Field(..., description="params of the user")

    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v):
        """Verifica che l'user_id sia lungo esattamente 7 caratteri"""
        if len(v) != 7:
            raise ValueError("user_id deve essere lungo esattamente 7 caratteri")
        return v