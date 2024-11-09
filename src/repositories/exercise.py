from typing import List
from src.models.exercise import Exercise as ExerciseModel
from src.schemas.exercise import Exercise

class ExerciseRepository:
    def __init__(self, db):
        self.db = db

    def get_all_excercises(self):
        return self.db.query(ExerciseModel).all()

    def get_excercise_by_id(self, id):
        return self.db.query(ExerciseModel).filter(ExerciseModel.id == id).first()

    def create_new_excercise(self, exercise: Exercise):
        new_excercise = ExerciseModel(**exercise.model_dump())

        self.db.add(new_excercise)
        self.db.commit()
        self.db.refresh(new_excercise)
        return new_excercise

    def delete_excercise(self, id):
        element = self.db.query(ExerciseModel).filter(ExerciseModel.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element
    
    def update_excercise(self, id: int, exercise: Exercise) -> dict:
        element = self.db.query(ExerciseModel).filter(ExerciseModel.id == id).first()
        element.name = exercise.name
        element.description = exercise.description
        element.image = exercise.image
        element.video = exercise.video
        element.dateAdded = exercise.dateAdded

        self.db.commit()
        self.db.refresh(element)
        return element