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
    max_users: int = Field(default=15, title="Número máximo de usuarios permitidos")
    current_users: int = Field(default=0, title="Número actual de usuarios")

    @validator("is_active")
    def is_active_must_be_boolean(cls, v):
        if not isinstance(v, bool):
            raise ValueError("El campo is_active debe ser booleano")
        return v
    
    @validator("is_premium")
    def is_premium_must_be_boolean(cls, v):
        if not isinstance(v, bool):
            raise ValueError("El campo is_premium debe ser booleano")
        return v
    
    @validator("max_users")
    def max_users_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("El número máximo de usuarios debe ser positivo")
        return v
    
    @validator("current_users")
    def current_users_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("El número actual de usuarios debe ser positivo")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_email": "hola@gmail.com",
                "gym_id": 1,
                "start_date": "2021-11-12",
                "final_date": "2021-12-12",
                "is_active": True,
                "is_premium": True,
                "max_users": 15,
                "current_users": 0
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