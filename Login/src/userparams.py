from pydantic import BaseModel, Field, field_validator


class UserParams(BaseModel):
    """Modello per i parametri dell'utente con range 1-5"""
    humor: int = Field(3, ge=1, le=5, example=3, description="Livello di umorismo (1-5)")
    empathy: int = Field(3, ge=1, le=5, example=3, description="Livello di empatia (1-5)")
    optimism: int = Field(3, ge=1, le=5, example=3, description="Livello di ottimismo (1-5)")

    @field_validator('humor', 'empathy', 'optimism')
    @classmethod
    def validate_params_range(cls, v, info):
        """Validazione aggiuntiva per i parametri"""
        if not 1 <= v <= 5:
            raise ValueError(f'{info.field_name} deve essere tra 1 e 5')
        return v

    def to_dict(self) -> dict:
        """Converte i parametri in dizionario"""
        return {
            "humor": self.humor,
            "empathy": self.empathy,
            "optimism": self.optimism
        }
