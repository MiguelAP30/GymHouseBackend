from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class Like(BaseModel):
    id: Optional[int] = Field(default=None, title="Id del like")
    user_email: Optional[str] = Field(default=None, title="Email del usuario")
    training_plan_id: int = Field(title="Id del plan de entrenamiento")
    is_like: bool = Field(default=True, title="True para like, False para dislike")
    
    @validator("training_plan_id")
    def training_plan_id_must_be_positive(cls, value):
        assert value > 0, ValueError("El id del plan de entrenamiento debe ser positivo")
        return value
    
    class Config:
        json_schema_extra = {
            "example": {
                "training_plan_id": 1,
                "is_like": True
            }
        }

class LikeResponse(BaseModel):
    """
    Modelo de respuesta para los likes/dislikes.
    Extiende el modelo Like para mantener la consistencia en las respuestas de la API.
    """
    id: int
    user_email: str
    training_plan_id: int
    is_like: bool

    class Config:
        orm_mode = True