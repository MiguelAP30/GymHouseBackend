from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class TrainingPlan(BaseModel):
    id: Optional[int] = Field(default=None, title="Id del plan de entrenamiento")
    name: str = Field(min_length=4, title="nombre del plan de entrenamiento", max_length=60)
    description: str = Field(min_length=4, title="Descripcion del plan de entrenamiento", max_length=200)
    tag_of_training_plan_id: Optional[int] = Field(default=None, title="Id de la etiqueta del plan de entrenamiento")
    user_email: Optional[str] = Field(default=None, title="Email del usuario")
    user_gym_id: Optional[int] = Field(default=None, title="Id de la relación usuario-gimnasio")
    is_visible: Optional[bool] = Field(default=False, title="Estado del plan de entrenamiento")
    is_gym_created: Optional[bool] = Field(default=False, title="Indica si el plan fue creado por un gimnasio")

class TrainingPlanCreate(BaseModel):
    name: str = Field(min_length=4, title="nombre del plan de entrenamiento", max_length=60)
    description: str = Field(min_length=4, title="Descripcion del plan de entrenamiento", max_length=200)
    tag_of_training_plan_id: Optional[int] = Field(default=None, title="Id de la etiqueta del plan de entrenamiento")
    user_email: str = Field(title="Email del usuario")
    is_visible: Optional[bool] = Field(default=False, title="Estado del plan de entrenamiento")
    is_gym_created: Optional[bool] = Field(default=False, title="Indica si el plan fue creado por un gimnasio")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "push pull legs",
                "description": "El push pull legs es un plan de entrenamiento que se basa en dividir los musculos en 3 grupos principales, los musculos que empujan, los musculos que jalan y las piernas",
                "tag_of_training_plan_id": 1,
                "user_email": "usuario@ejemplo.com",
                "is_visible": True,
                "is_gym_created": False
            }
        }

class TrainingPlanCreateByGym(BaseModel):
    name: str = Field(min_length=4, max_length=60, title="Nombre del plan de entrenamiento")
    description: str = Field(min_length=4, max_length=200, title="Descripción del plan de entrenamiento")
    tag_of_training_plan_id: int = Field(title="ID de la etiqueta del plan")
    user_email: str = Field(title="Email del usuario destino")
    is_visible: bool = Field(default=False, title="Visibilidad del plan")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "plan full body",
                "description": "Rutina de cuerpo completo de 3 días",
                "tag_of_training_plan_id": 1,
                "user_email": "user1@gmail.com",
                "is_visible": True
            }
        }

class TrainingPlanUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=4, max_length=60, title="Nombre del plan")
    description: Optional[str] = Field(None, min_length=4, max_length=200, title="Descripción del plan")
    tag_of_training_plan_id: Optional[int] = Field(None, title="Etiqueta del plan")
    is_visible: Optional[bool] = Field(None, title="Visibilidad del plan")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Plan actualizado",
                "description": "Rutina mejorada de 5 días",
                "tag_of_training_plan_id": 2,
                "is_visible": True
            }
        }

class PaginatedTrainingPlanResponse(BaseModel):
    items: List[TrainingPlan]
    total: int
    page: int
    size: int
    pages: int