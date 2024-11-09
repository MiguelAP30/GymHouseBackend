from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class ExercisePerWeekDay(BaseModel):
    id: Optional[int] = Field(default=None, title="Id del ejercicio")
    week_day_id: int = Field(title="Id del dia de la semana")
    detail_exercise_id: int = Field(title="Id del ejercicio en el plan de entrenamiento")
    training_plan_id: int = Field(default=None, title="Id del plan de entrenamiento")
    class Config:
        json_schema_extra = {
            "example": {
                "week_day_id": 1,
                "detail_exercise_id": 1,
                "training_plan_id": 1
            }
        }
