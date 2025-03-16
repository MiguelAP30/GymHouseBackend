from typing import List
from src.models.series_pr_exercise import SeriesPrExercise as series_pr_exercise
from src.models.dropset_pr_exercise import DropSetPrExercise as dropset_pr_exercise
from src.schemas.series_pr_exercise import SeriesPrExercise

class SeriesPrExerciseRepository():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all_series_pr_exercise(self, history_pr_exercise_id: int) -> List[SeriesPrExercise]:
        """
        Obtiene todas las series PR de un historial específico.
        """
        query = self.db.query(series_pr_exercise).filter(series_pr_exercise.history_pr_exercise_id == history_pr_exercise_id)
        return query.all()
    
    def create_new_series_pr_exercise(self, series_pr_exercise_data: SeriesPrExercise) -> SeriesPrExercise:
        """
        Crea una nueva serie PR.
        """
        new_series = series_pr_exercise(
            history_pr_exercise_id=series_pr_exercise_data.history_pr_exercise_id,
            weight=series_pr_exercise_data.weight,
            reps=series_pr_exercise_data.reps
        )
        self.db.add(new_series)
        self.db.commit()
        self.db.refresh(new_series)
        return new_series
    
    def remove_series_pr_exercise(self, id: int) -> dict:
        """
        Elimina una serie PR específica.
        """
        element = self.db.query(series_pr_exercise).filter(series_pr_exercise.id == id).first()
        if element:
            self.db.delete(element)
            self.db.commit()
        return element
    
    def get_series_pr_exercise_by_id(self, id: int) -> SeriesPrExercise:
        """
        Obtiene una serie PR específica por su ID.
        """
        return self.db.query(series_pr_exercise).filter(series_pr_exercise.id == id).first()
    
    def update_series_pr_exercise(self, id: int, series_pr_exercise_data: SeriesPrExercise) -> SeriesPrExercise:
        """
        Actualiza una serie PR específica.
        """
        element = self.db.query(series_pr_exercise).filter(series_pr_exercise.id == id).first()
        if element:
            element.weight = series_pr_exercise_data.weight
            element.reps = series_pr_exercise_data.reps
            self.db.commit()
            self.db.refresh(element)
        return element 