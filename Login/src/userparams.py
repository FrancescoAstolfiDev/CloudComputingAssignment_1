from pydantic import BaseModel, Field, field_validator


class UserParams(BaseModel):
    """model used for the user params, easy to add new params"""
    humor: int = Field(3, ge=1, le=5, example=3, description="Humor Level (1-5)")
    empathy: int = Field(3, ge=1, le=5, example=3, description="Emphathy Level (1-5)")
    optimism: int = Field(3, ge=1, le=5, example=3, description="Optimism Level (1-5)")

    @field_validator('humor', 'empathy', 'optimism')
    @classmethod
    def validate_params_range(cls, v, info):
        """validation of the params range"""
        if not 1 <= v <= 5:
            raise ValueError(f'{info.field_name} deve essere tra 1 e 5')
        return v

    def to_dict(self) -> dict:
        """ Convert the model to a dictionary"""
        return {
            "humor": self.humor,
            "empathy": self.empathy,
            "optimism": self.optimism
        }
