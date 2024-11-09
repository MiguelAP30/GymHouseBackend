from pydantic import BaseModel, Field, model_validator
from typing import Optional

class ExerciseMuscle(BaseModel):
    id: Optional[int] = Field(default=None, title="Id de la maquina de ejercicios")
    specific_muscle_id: int = Field(title="Musculo especifico")
    exercise_id: int = Field(title="Id del ejercicio")
    rate: int = Field(ge=0, le=10,title="Calificacion del ejercicio")
    class Config:
        json_schema_extra = {
            "example": {
                "specific_muscle_id": 1,
                "exercise_id": 1,
                "rate": 10
            }
        }