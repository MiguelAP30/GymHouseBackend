from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class Profile(BaseModel):
    id: Optional[int] = Field(default=None, title="Id del perfil")
    user_email: str = Field(title="Email del usuario")
    weight: float = Field(title="Peso")
    height: float = Field(title="Altura")
    physical_activity: int = Field(title="Actividad física")
    date: str = Field(title="Fecha")
    
    @validator("weight")
    def weight_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("El peso debe ser positivo")
        return v
    
    @validator("height")
    def height_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("La altura debe ser positiva")
        return v
    
    @validator("physical_activity")
    def physical_activity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("La actividad física debe ser positiva")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_email": "hola@gmail.com",
                "weight": 70.0,
                "height": 1.70,
                "physical_activity": 1,
                "date": "2021-11-12"
            }
        }
        