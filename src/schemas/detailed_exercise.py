from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class DetailedExercise(BaseModel):
    id: Optional[int] = Field(default=None, title="Id del ejercicio detallado")
    exercice_muscle_id: int = Field(title="Id de la tabla de ejercicios musculos")
    sets: int = Field(ge=1,title="Cantidad de series", le=10)
    reps: int = Field(ge=1,title="Cantidad de repeticiones", le=100)
    rest: float = Field(ge=1, title="Tiempo de descanso", le=1000)

    @validator("sets")
    def sets_must_be_int(cls, v):
        if not isinstance(v, int):
            raise ValueError("las series deben ser un entero")
        return v
    
    @validator("reps")
    def reps_must_be_int(cls, v):
        if not isinstance(v, int):
            raise ValueError("las repeticiones deben ser un entero")
        return v
    
    @validator("rest")
    def rest_must_be_float(cls, v):
        if not isinstance(v, float):
            raise ValueError("el tiempo de descanso debe ser un float")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "exercice_muscle_id": 1,
                "sets": 3,
                "reps": 10,
                "rest": 60.0
            }
        }