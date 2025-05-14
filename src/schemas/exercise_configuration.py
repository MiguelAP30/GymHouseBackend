from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class ExerciseConfiguration(BaseModel):
    id: Optional[int] = Field(default=None, title="Id de la configuración del ejercicio")
    exercise_id: int = Field(title="Id del ejercicio")
    workout_day_exercise_id: int = Field(title="Id del ejercicio por día de la semana")
    sets: int = Field(ge=1,title="Cantidad de series", le=10)
    repsHigh: int = Field(ge=1,title="Cantidad de repeticiones", le=100)
    repsLow: Optional[int] = Field(ge=1,title="Cantidad de repeticiones", le=100)
    rest: float = Field(ge=1, title="Tiempo de descanso", le=1000)
    notes: Optional[str] = Field(default=None, title="Notas")
    class Config:
        json_schema_extra = {
            "example": {
                "exercise_id": 1,
                "workout_day_exercise_id": 1,
                "sets": 3,
                "repsHigh": 15,
                "repsLow": 10,
                "rest": 60.0,
                "notes": "Realizar con cuidado"
            }
        }