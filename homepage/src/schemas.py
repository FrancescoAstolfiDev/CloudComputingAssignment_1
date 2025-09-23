from pydantic import BaseModel, Field, EmailStr, field_validator
from .userparams import UserParams

class User(BaseModel):
    user_id: str
    params: UserParams = Field(..., description="Param of the user")

    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v):
        """Verifica che l'user_id sia lungo esattamente 7 caratteri"""
        if len(v) != 7:
            raise ValueError("user_id deve essere lungo esattamente 7 caratteri")
        return v
