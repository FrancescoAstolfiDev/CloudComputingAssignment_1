from pydantic import BaseModel, Field, EmailStr
from .userparams import UserParams

class UserBasicInfo(BaseModel):
    user_id: str
    params: UserParams = Field(..., description="Param of the user")

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    identifier: str  # può essere user_id o email
    password: str