from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional
from datetime import date

class UserGym(BaseModel):
    id: Optional[int] = Field(default=None, title="Id de la relación entre usuario y gimnasio")
    user_email: str = Field(title="Email del usuario")
    gym_id: int = Field(title="Id del gimnasio")
    start_date: date = Field(title="Fecha de inicio")
    final_date: date = Field(title="Fecha de finalización")
    is_active: bool = Field(default=True, title="¿Está activo?")
    is_premium: bool = Field(default=False, title="¿Es premium?")
    class Config:
        json_schema_extra = {
            "example": {
                "user_email": "hola@gmail.com",
                "gym_id": 1,
                "start_date": "2021-11-12",
                "final_date": "2021-12-12",
                "is_active": True,
                "is_premium": True,
            }
        }

class UserGymCreate(BaseModel):
    user_email: str = Field(title="Email del usuario")
    gym_id: int = Field(title="Id del gimnasio")
    start_date: date = Field(title="Fecha de inicio")
    final_date: date = Field(title="Fecha de finalización")

    class Config:
        json_schema_extra = {
            "example": {
                "user_email": "hola@gmail.com",
                "gym_id": 1,
                "start_date": "2021-11-12",
                "final_date": "2021-12-12"
            }
        }

class UserGymUpdateFinalDate(BaseModel):
    final_date: date = Field(title="Nueva fecha de finalización")

    class Config:
        json_schema_extra = {
            "example": {
                "final_date": "2025-06-30"
            }
        }