from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class WorkoutDayExercise(BaseModel):
    id: Optional[int] = Field(default=None, title="Id del ejercicio")
    week_day_id: int = Field(title="Id del dia de la semana")
    training_plan_id: int = Field(default=None, title="Id del plan de entrenamiento")
    class Config:
        json_schema_extra = {
            "example": {
                "week_day_id": 1,
                "training_plan_id": 1
            }
        }
