from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class Star(BaseModel):
    id: Optional[int] = Field(default=None, title="Id de la estrella")
    user_email: str = Field(title="Email del usuario")
    training_plan_id: int = Field(title="Id del plan de entrenamiento")
    
    @validator("training_plan_id")
    def training_plan_id_must_be_positive(cls, value):
        assert value > 0, ValueError("El id del plan de entrenamiento debe ser positivo")
        return value
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_email": "hola@gmail.com",
                "training_plan_id": 1
            }
        }