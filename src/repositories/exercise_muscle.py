from typing import List

from sqlalchemy import desc
from src.schemas.exercise_muscle import ExerciseMuscle
from src.models.exercise_muscle import ExerciseMuscle as ExerciseMuscleModel
from src.models.muscle import Muscle as MuscleModel
from src.models.machine import Machine as MachineModel
from src.models.specific_muscle import SpecificMuscle as SpecificMuscleModel
from src.models.exercise import Exercise as ExerciseModel



class ExerciseMuscleRepository():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all_excercise_muscle_by_rate(self) -> List[ExerciseMuscle]:
        query = self.db.query(ExerciseMuscleModel).order_by(desc(ExerciseMuscleModel.rate))
        return query.all()
    
    def get_excercise_muscle_machine_by_rate(self, machine_id: int) -> List[ExerciseMuscle]:
        query = (
            self.db.query(ExerciseMuscleModel)
            .join(ExerciseModel, ExerciseMuscleModel.exercise_id == ExerciseModel.id)
            .join(MachineModel, ExerciseModel.machine_id == MachineModel.id)
            .filter(MachineModel.id == machine_id)
            .order_by(desc(ExerciseMuscleModel.rate))
        )
        return query.all()
    
    def get_excercise_muscle_specific_muscle_by_rate(self, specific_muscle_id: int) -> List[ExerciseMuscle]:
        query = (
            self.db.query(ExerciseMuscleModel)
            .filter(ExerciseMuscleModel.specific_muscle_id == specific_muscle_id)
            .order_by(desc(ExerciseMuscleModel.rate))
        )
        return query.all()
    
    def get_excercise_muscle_by_muscle_by_rate(self, muscle_id: int) -> List[ExerciseMuscle]:
        query = (
            self.db.query(ExerciseMuscleModel)
            .join(SpecificMuscleModel)
            .filter(SpecificMuscleModel.muscle_id == muscle_id)
            .order_by(desc(ExerciseMuscleModel.rate))
        )
        return query.all()
    
    def get_excercise_muscle_by_id(self, id: int) -> ExerciseMuscle:
        element = self.db.query(ExerciseMuscleModel).filter(ExerciseMuscleModel.id == id).first()
        return element
    
    def create_new_excercise_muscle(self, exercise_muscle: ExerciseMuscle) -> ExerciseMuscle:
        new_excercise_muscle = ExerciseMuscleModel(**exercise_muscle.model_dump())
        self.db.add(new_excercise_muscle)
        self.db.commit()
        self.db.refresh(new_excercise_muscle)
        return new_excercise_muscle
    
    def delete_excercise_muscle(self, id: int) -> ExerciseMuscle:
        element = self.db.query(ExerciseMuscleModel).filter(ExerciseMuscleModel.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element
    
    def update_rate_excercise_muscle(self, id: int, rate: int) -> ExerciseMuscle:
        element = self.db.query(ExerciseMuscleModel).filter(ExerciseMuscleModel.id == id).first()
        element.rate = rate
        self.db.commit()
        self.db.refresh(element)
        return element
