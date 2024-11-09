from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class WeekDay(BaseModel):
    id: Optional[int] = Field(default=None, title="Id del dia de la semana")
    name: str = Field(min_length=4, title="nombre del dia de la semana", max_length=20)

    @validator("name")
    def name_must_not_be_empty(cls, value):
        assert isinstance(value,str), ValueError("el nombre debe ser un string")
        return value
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "lunes"
            }
        }