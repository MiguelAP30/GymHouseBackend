from typing import List
from src.models.series_pr_exercise import SeriesPrExercise as series_pr_exercise
from src.models.dropset_pr_exercise import DropSetPrExercise as dropset_pr_exercise
from src.models.history_pr_exercise import HistoryPrExercise as history_pr_exercise
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
    
    def create_new_series_pr_exercise(self, series_pr_exercise_data: SeriesPrExercise, user_email: str) -> SeriesPrExercise:
        """
        Crea una nueva serie PR.
        """
        # Verificar que el usuario es el dueño del historial
        history = self.db.query(history_pr_exercise).filter(
            history_pr_exercise.id == series_pr_exercise_data.history_pr_exercise_id,
            history_pr_exercise.user_email == user_email
        ).first()
        
        if not history:
            raise ValueError("No tienes permiso para crear series en este historial")
            
        new_series = series_pr_exercise(
            history_pr_exercise_id=series_pr_exercise_data.history_pr_exercise_id,
            weight=series_pr_exercise_data.weight,
            reps=series_pr_exercise_data.reps
        )
        self.db.add(new_series)
        self.db.commit()
        self.db.refresh(new_series)
        return new_series
    
    def remove_series_pr_exercise(self, id: int, user_email: str) -> dict:
        """
        Elimina una serie PR específica.
        """
        series = self.db.query(series_pr_exercise).filter(series_pr_exercise.id == id).first()
        if series:
            history = self.db.query(history_pr_exercise).filter(
                history_pr_exercise.id == series.history_pr_exercise_id,
                history_pr_exercise.user_email == user_email
            ).first()
            
            if not history:
                raise ValueError("No tienes permiso para eliminar esta serie")
                
            self.db.delete(series)
            self.db.commit()
        return series
    
    def get_series_pr_exercise_by_id(self, id: int) -> SeriesPrExercise:
        """
        Obtiene una serie PR específica por su ID.
        """
        return self.db.query(series_pr_exercise).filter(series_pr_exercise.id == id).first()
    
    def update_series_pr_exercise(self, id: int, series_pr_exercise_data: SeriesPrExercise, user_email: str) -> SeriesPrExercise:
        """
        Actualiza una serie PR específica.
        """
        series = self.db.query(series_pr_exercise).filter(series_pr_exercise.id == id).first()
        if series:
            history = self.db.query(history_pr_exercise).filter(
                history_pr_exercise.id == series.history_pr_exercise_id,
                history_pr_exercise.user_email == user_email
            ).first()
            
            if not history:
                raise ValueError("No tienes permiso para actualizar esta serie")
                
            series.weight = series_pr_exercise_data.weight
            series.reps = series_pr_exercise_data.reps
            series.tipo_serie = series_pr_exercise_data.tipo_serie
            series.rpe = series_pr_exercise_data.rpe
            series.orden_serie = series_pr_exercise_data.orden_serie
            series.notas_serie = series_pr_exercise_data.notas_serie
            self.db.commit()
            self.db.refresh(series)
        return series 