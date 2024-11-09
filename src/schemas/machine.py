from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class Machine(BaseModel):
    id: Optional[int] = Field(default=None, title="Id de la maquina")
    name: str = Field(min_length=4, title="nombre de la maquina", max_length=50)
    description: str = Field(min_length=4, title="descripción de la maquina ", max_length=200)
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Barra",
                "description": "La barra es un elemento de entrenamiento"
            }
        }