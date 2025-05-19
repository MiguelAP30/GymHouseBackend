from pydantic import BaseModel, Field, validator
from typing import Optional

class DropSetPrExercise(BaseModel):
    id: Optional[int] = Field(default=None, title="Id del dropset PR")
    serie_pr_exercise_id: int = Field(title="Id de la serie PR")
    weight: float = Field(title="Peso levantado")
    reps: int = Field(title="Repeticiones")
    orden_dropset: Optional[int] = Field(default=None, title="Orden del dropset", gt=0)
    class Config:
        json_schema_extra = {
            "example": {
                "serie_pr_exercise_id": 1,
                "weight": 80.0,
                "reps": 8,
                "orden_dropset": 1
            }
        }

class UpdateDropSetPrExercise(BaseModel):
    weight: float = Field(title="Peso levantado")
    reps: int = Field(title="Repeticiones")
    orden_dropset: Optional[int] = Field(default=None, title="Orden del dropset", gt=0)
    class Config:
        json_schema_extra = {
            "example": {
                "weight": 80.0,
                "reps": 8,
                "orden_dropset": 1
            }
        } 