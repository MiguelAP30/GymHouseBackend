from typing import List, Union

from sqlalchemy import desc
from src.schemas.exercise_muscle import ExerciseMuscle, ExerciseMuscleAssignment
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
    
    def update_exercise_muscle(self, id: int, rate_or_exercise: Union[int, ExerciseMuscle]) -> ExerciseMuscle:
        element = self.db.query(ExerciseMuscleModel).filter(ExerciseMuscleModel.id == id).first()
        
        # Verificamos si rate_or_exercise es un objeto ExerciseMuscle o un valor numérico
        if isinstance(rate_or_exercise, ExerciseMuscle):
            # Actualizamos todos los campos del objeto ExerciseMuscle
            for key, value in rate_or_exercise.model_dump(exclude={'id'}).items():
                setattr(element, key, value)
        else:
            # Si es solo un valor numérico, actualizamos solo el rate
            element.rate = rate_or_exercise
            
        self.db.commit()
        self.db.refresh(element)
        return element
        
    def assign_muscles_to_exercise(self, assignment: ExerciseMuscleAssignment) -> List[ExerciseMuscle]:
        # Primero eliminamos las asignaciones existentes para este ejercicio
        existing_assignments = self.db.query(ExerciseMuscleModel).filter(
            ExerciseMuscleModel.exercise_id == assignment.exercise_id
        ).all()
        
        for existing in existing_assignments:
            self.db.delete(existing)
        
        # Creamos las nuevas asignaciones
        new_assignments = []
        for muscle_assignment in assignment.muscle_assignments:
            new_assignment = ExerciseMuscleModel(
                exercise_id=assignment.exercise_id,
                specific_muscle_id=muscle_assignment["specific_muscle_id"],
                rate=muscle_assignment["rate"]
            )
            self.db.add(new_assignment)
            new_assignments.append(new_assignment)
        
        self.db.commit()
        
        # Refrescamos los objetos para obtener los IDs generados
        for assignment in new_assignments:
            self.db.refresh(assignment)
            
        return new_assignments
        
    def get_muscles_by_exercise(self, exercise_id: int) -> List[ExerciseMuscle]:
        query = (
            self.db.query(ExerciseMuscleModel)
            .filter(ExerciseMuscleModel.exercise_id == exercise_id)
            .order_by(desc(ExerciseMuscleModel.rate))
        )
        return query.all()
