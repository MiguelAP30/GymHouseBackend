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

class DropSetCreate(BaseModel):
    weight: float = Field(title="Peso levantado")
    reps: int = Field(title="Repeticiones")
    orden_dropset: Optional[int] = Field(default=None, title="Orden del dropset", gt=0)

class SeriesCreate(BaseModel):
    weight: float = Field(title="Peso levantado")
    reps: int = Field(title="Repeticiones")
    tipo_serie: Optional[str] = Field(default=None, title="Tipo de serie", max_length=50)
    rpe: Optional[float] = Field(default=None, title="RPE", ge=1, le=10)
    orden_serie: Optional[int] = Field(default=None, title="Orden de la serie", gt=0)
    notas_serie: Optional[str] = Field(default=None, title="Notas de la serie", max_length=500)
    dropsets: Optional[List[DropSetCreate]] = Field(default_factory=list, title="Lista de dropsets asociados")

class FullHistoryPrExerciseCreate(BaseModel):
    exercise_id: int = Field(title="Id del ejercicio")
    date: str = Field(title="Fecha")
    notas: Optional[str] = Field(default=None, title="Notas del historial", max_length=500)
    tipo_sesion: Optional[str] = Field(default=None, title="Tipo de sesión", max_length=50)
    series: Optional[List[SeriesCreate]] = Field(default_factory=list, title="Lista de series del ejercicio")

    class Config:
        json_schema_extra = {
            "example": {
                "exercise_id": 1,
                "date": "2025-05-19",
                "notas": "Sesión de fuerza",
                "tipo_sesion": "Fuerza",
                "series": [
                    {
                        "weight": 100.0,
                        "reps": 8,
                        "tipo_serie": "Principal",
                        "rpe": 8,
                        "orden_serie": 1,
                        "notas_serie": "Buena ejecución",
                        "dropsets": [
                            {
                                "weight": 80.0,
                                "reps": 10,
                                "orden_dropset": 1
                            },
                            {
                                "weight": 60.0,
                                "reps": 12,
                                "orden_dropset": 2
                            }
                        ]
                    },
                    {
                        "weight": 90.0,
                        "reps": 10,
                        "tipo_serie": "Accesoria",
                        "rpe": 7,
                        "orden_serie": 2,
                        "notas_serie": "Serie ligera",
                        "dropsets": []
                    }
                ]
            }
        }