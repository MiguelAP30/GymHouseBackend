from typing import List
from src.models.dropset_pr_exercise import DropSetPrExercise as dropset_pr_exercise
from src.schemas.dropset_pr_exercise import DropSetPrExercise

class DropSetPrExerciseRepository():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all_dropset_pr_exercise(self, serie_pr_exercise_id: int) -> List[DropSetPrExercise]:
        """
        Obtiene todos los dropsets PR de una serie específica.
        """
        query = self.db.query(dropset_pr_exercise).filter(dropset_pr_exercise.serie_pr_exercise_id == serie_pr_exercise_id)
        return query.all()
    
    def create_new_dropset_pr_exercise(self, dropset_pr_exercise_data: DropSetPrExercise) -> DropSetPrExercise:
        """
        Crea un nuevo dropset PR.
        """
        new_dropset = dropset_pr_exercise(
            serie_pr_exercise_id=dropset_pr_exercise_data.serie_pr_exercise_id,
            weight=dropset_pr_exercise_data.weight,
            reps=dropset_pr_exercise_data.reps
        )
        self.db.add(new_dropset)
        self.db.commit()
        self.db.refresh(new_dropset)
        return new_dropset
    
    def remove_dropset_pr_exercise(self, id: int) -> dict:
        """
        Elimina un dropset PR específico.
        """
        element = self.db.query(dropset_pr_exercise).filter(dropset_pr_exercise.id == id).first()
        if element:
            self.db.delete(element)
            self.db.commit()
        return element
    
    def get_dropset_pr_exercise_by_id(self, id: int) -> DropSetPrExercise:
        """
        Obtiene un dropset PR específico por su ID.
        """
        return self.db.query(dropset_pr_exercise).filter(dropset_pr_exercise.id == id).first()
    
    def update_dropset_pr_exercise(self, id: int, dropset_pr_exercise_data: DropSetPrExercise) -> DropSetPrExercise:
        """
        Actualiza un dropset PR específico.
        """
        element = self.db.query(dropset_pr_exercise).filter(dropset_pr_exercise.id == id).first()
        if element:
            element.weight = dropset_pr_exercise_data.weight
            element.reps = dropset_pr_exercise_data.reps
            self.db.commit()
            self.db.refresh(element)
        return element 