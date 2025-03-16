from pydantic import BaseModel, Field, validator
from typing import Optional

class SeriesPrExercise(BaseModel):
    id: Optional[int] = Field(default=None, title="Id de la serie PR")
    history_pr_exercise_id: int = Field(title="Id del historial PR")
    weight: float = Field(title="Peso levantado")
    reps: int = Field(title="Repeticiones")

    @validator("weight")
    def weight_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("El peso debe ser positivo")
        return v
    
    @validator("reps")
    def reps_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Las repeticiones deben ser positivas")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "history_pr_exercise_id": 1,
                "weight": 100.0,
                "reps": 10
            }
        } 