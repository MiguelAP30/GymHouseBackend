from pydantic import BaseModel, Field, model_validator
from typing import Optional, List

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

class ExerciseMuscleAssignment(BaseModel):
    exercise_id: int = Field(title="Id del ejercicio")
    muscle_assignments: List[dict] = Field(title="Lista de asignaciones de músculos con sus tasas")
    
    class Config:
        json_schema_extra = {
            "example": {
                "exercise_id": 1,
                "muscle_assignments": [
                    {"specific_muscle_id": 1, "rate": 8},
                    {"specific_muscle_id": 2, "rate": 5},
                    {"specific_muscle_id": 3, "rate": 3}
                ]
            }
        }