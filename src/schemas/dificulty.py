from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class Dificulty(BaseModel):
    id: int = Field(default=None, title="Id de la dificultad")
    name: str = Field(title="Nombre de la dificultad")
    
    @validator("name")
    def name_must_be_str(cls, v):
        if not isinstance(v, str):
            raise ValueError("El nombre debe ser una cadena de texto")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Fácil"
            }
        }