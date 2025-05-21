from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class ProfileBase(BaseModel):
    weight: float = Field(title="Peso")
    height: float = Field(title="Altura")
    physical_activity: int = Field(title="Actividad física")
    fat: Optional[float] = Field(default=None, title="Grasa corporal")
    muscle: Optional[float] = Field(default=None, title="Masa muscular")
    chest: Optional[float] = Field(default=None, title="Medida del pecho")
    waist: Optional[float] = Field(default=None, title="Medida de la cintura")
    hips: Optional[float] = Field(default=None, title="Medida de las caderas")
    biceps: Optional[float] = Field(default=None, title="Medida de los bíceps")
    thigh: Optional[float] = Field(default=None, title="Medida de los muslos")
    notes: Optional[str] = Field(default=None, title="Notas")
    date: str = Field(title="Fecha")

    class Config:
        from_attributes = True

class ProfileUpdate(ProfileBase):
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "weight": 70.0,
                "height": 1.70,
                "physical_activity": 1,
                "fat": 15.0,
                "muscle": 30.0,
                "chest": 100.0,
                "waist": 80.0,
                "hips": 90.0,
                "biceps": 30.0,
                "thigh": 50.0,
                "notes": "Notas del perfil",
                "date": "2021-11-12"
            }
        }

class Profile(ProfileBase):
    id: Optional[int] = Field(default=None, title="Id del perfil")
    user_email: Optional[str] = Field(default=None, title="Email del usuario")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "weight": 70.0,
                "height": 1.70,
                "physical_activity": 1,
                "fat": 15.0,
                "muscle": 30.0,
                "chest": 100.0,
                "waist": 80.0,
                "hips": 90.0,
                "biceps": 30.0,
                "thigh": 50.0,
                "notes": "Notas del perfil",
                "date": "2021-11-12"
            }
        }
        