from pydantic import BaseModel, Field, EmailStr
from .userparams import UserParams

class UserResponse(BaseModel):
    user_id: str
    params: UserParams = Field(..., description="Param of the user")

class UserCreate(BaseModel):
    password: str
    email: EmailStr



class LoginRequest(BaseModel):
    identifier: str  # può essere user_id o email
    password: str