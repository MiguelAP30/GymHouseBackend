from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class Muscle(BaseModel):
    id: Optional[int] = Field(default=None, title="Id del musculo")
    name: str = Field(min_length=4, title="nombre del musculo", max_length=50)
    description: str = Field(min_length=4, title="Descripcion del musculo", max_length=200)

    @validator("name")
    def name_must_contain_letter(cls, v):
        assert isinstance(v, str), ValueError("el nombre debe ser un string")
        return v
    
    @validator("description")
    def description_must_contain_letter(cls, v):
        if v:
            assert isinstance(v, str), ValueError("la descripcion debe ser un string")
        return v
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Pectoral",
                "description": "El pectoral es un musculo que se encuentra en la parte delantera del torax"
            }
        }
