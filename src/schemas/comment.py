from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class Comment(BaseModel):
    id: Optional[int] = Field(default=None, title="Id del comentario")
    user_email: str = Field(title="Email del usuario")
    training_plan_id: int = Field(title="Id del plan de entrenamiento")
    content: str = Field(title="Contenido del comentario")
    date: str = Field(title="Fecha del comentario")

    @validator("training_plan_id")
    def training_plan_id_must_be_positive(cls, value):
        assert value > 0, ValueError("El id del plan de entrenamiento debe ser positivo")
        return value
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_email": "hola@gmail.com",
                "training_plan_id": 1,
                "content": "Excelente plan de entrenamiento",
                "date": "2021-11-12"
            }
        }