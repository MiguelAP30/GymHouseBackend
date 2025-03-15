from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class TrainingPlan(BaseModel):
    id: Optional[int] = Field(default=None, title="Id del plan de entrenamiento")
    name: str = Field(min_length=4, title="nombre del plan de entrenamiento", max_length=60)
    description: str = Field(min_length=4, title="Descripcion del plan de entrenamiento", max_length=200)
    tag_of_training_plan_id: Optional[int] = Field(default=None, title="Id de la etiqueta del plan de entrenamiento")
    user_email: Optional[str] = Field(default=None, title="Email del usuario")
    is_visible: Optional[bool] = Field(default=False, title="Estado del plan de entrenamiento")

    @validator("name")
    def name_must_not_be_empty(cls, value):
        assert isinstance(value,str), ValueError("el nombre debe ser un string")
        return value
    
    @validator("description")
    def description_must_not_be_empty(cls, value):
        assert isinstance(value,str), ValueError("la descripcion debe ser un string")
        return value
    class Config:
        json_schema_extra = {
            "example": {
                "name": "push pull legs",
                "description": "El push pull legs es un plan de entrenamiento que se basa en dividir los musculos en 3 grupos principales, los musculos que empujan, los musculos que jalan y las piernas",
                "tag_of_training_plan_id": 1,
                "is_visible": True
            }
        }