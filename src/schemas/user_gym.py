from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class UserGym(BaseModel):
    id: Optional[int] = Field(default=None, title="Id de la relación entre usuario y gimnasio")
    user_email: str = Field(title="Email del usuario")
    gym_id: int = Field(title="Id del gimnasio")
    start_date: str = Field(title="Fecha de inicio")
    final_date: str = Field(title="Fecha de finalización")
    is_active: bool = Field(title="¿Está activo?")

    @validator("is_active")
    def is_active_must_be_boolean(cls, v):
        if not isinstance(v, bool):
            raise ValueError("El campo is_active debe ser booleano")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_email": "hola@gmail.com",
                "gym_id": 1,
                "start_date": "2021-11-12",
                "final_date": "2021-12-12",
                "is_active": True
            }
        }