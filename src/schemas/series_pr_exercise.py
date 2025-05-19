from pydantic import BaseModel, Field, validator
from typing import Optional

class SeriesPrExercise(BaseModel):
    id: Optional[int] = Field(default=None, title="Id de la serie PR")
    history_pr_exercise_id: int = Field(title="Id del historial PR")
    weight: float = Field(title="Peso levantado")
    reps: int = Field(title="Repeticiones")
    tipo_serie: Optional[str] = Field(default=None, title="Tipo de serie", max_length=50)
    rpe: Optional[float] = Field(default=None, title="RPE", ge=1, le=10)
    orden_serie: Optional[int] = Field(default=None, title="Orden de la serie", gt=0)
    notas_serie: Optional[str] = Field(default=None, title="Notas de la serie", max_length=500)
    class Config:
        json_schema_extra = {
            "example": {
                "history_pr_exercise_id": 1,
                "weight": 100.0,
                "reps": 10,
                "tipo_serie": "Principal",
                "rpe": 8.5,
                "orden_serie": 1,
                "notas_serie": "Notas de la serie"
            }
        }

class UpdateSeriesPrExercise(BaseModel):
    weight: float = Field(title="Peso levantado")
    reps: int = Field(title="Repeticiones")
    tipo_serie: Optional[str] = Field(default=None, title="Tipo de serie", max_length=50)
    rpe: Optional[float] = Field(default=None, title="RPE", ge=1, le=10)
    orden_serie: Optional[int] = Field(default=None, title="Orden de la serie", gt=0)
    notas_serie: Optional[str] = Field(default=None, title="Notas de la serie", max_length=500)
    class Config:
        json_schema_extra = {
            "example": {
                "weight": 100.0,
                "reps": 10,
                "tipo_serie": "Principal",
                "rpe": 8.5,
                "orden_serie": 1,
                "notas_serie": "Notas de la serie"
            }
        } 