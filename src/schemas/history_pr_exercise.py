from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional
from datetime import date
class HistoryPrExercise(BaseModel):
    id: Optional[int] = Field(default=None, title="Id del historial de PR de ejercicio")
    user_email: Optional[str] = Field(default=None, title="Email del usuario")
    exercise_id: int = Field(title="Id del ejercicio")
    date: str = Field(title="Fecha")
    notas: Optional[str] = Field(default=None, title="Notas del historial", max_length=500)
    tipo_sesion: Optional[str] = Field(default=None, title="Tipo de sesión", max_length=50)
    
    class Config:
        json_schema_extra = {
            "example": {
                "exercise_id": 1,
                "date": "2021-11-12",
                "notas": "Notas de la sesión",
                "tipo_sesion": "Fuerza"
            }
        }

class HistoryPrExerciseUpdate(BaseModel):
    notas: Optional[str] = Field(default=None, title="Notas del historial", max_length=500)
    tipo_sesion: Optional[str] = Field(default=None, title="Tipo de sesión", max_length=50)

    class Config:
        json_schema_extra = {
            "example": {
                "notas": "Actualización de notas",
                "tipo_sesion": "Resistencia"
            }
        }
