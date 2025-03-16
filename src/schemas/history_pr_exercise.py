from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional
from datetime import date

class DropSetPrExercise(BaseModel):
    id: Optional[int] = Field(default=None, title="Id del dropset PR")
    serie_pr_exercise_id: int = Field(title="Id de la serie PR")
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
                "serie_pr_exercise_id": 1,
                "weight": 80.0,
                "reps": 8
            }
        }

class SeriesPrExercise(BaseModel):
    id: Optional[int] = Field(default=None, title="Id de la serie PR")
    history_pr_exercise_id: int = Field(title="Id del historial PR")
    weight: float = Field(title="Peso levantado")
    reps: int = Field(title="Repeticiones")
    dropsets: Optional[List[DropSetPrExercise]] = Field(default=None, title="Dropsets de la serie")

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
                "reps": 10,
                "dropsets": [
                    {
                        "weight": 80.0,
                        "reps": 8
                    }
                ]
            }
        }

class HistoryPrExercise(BaseModel):
    id: Optional[int] = Field(default=None, title="Id del historial de PR de ejercicio")
    user_email: str = Field(title="Email del usuario")
    exercise_id: int = Field(title="Id del ejercicio")
    date: str = Field(title="Fecha")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_email": "hola@gmail.com",
                "exercise_id": 1,
                "date": "2021-11-12"
            }
        }

