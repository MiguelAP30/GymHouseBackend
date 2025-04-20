from typing import List
from src.models.dropset_pr_exercise import DropSetPrExercise as dropset_pr_exercise
from src.models.series_pr_exercise import SeriesPrExercise as series_pr_exercise
from src.models.history_pr_exercise import HistoryPrExercise as history_pr_exercise
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
    
    def create_new_dropset_pr_exercise(self, dropset_pr_exercise_data: DropSetPrExercise, user_email: str) -> DropSetPrExercise:
        """
        Crea un nuevo dropset PR.
        """
        # Verificar que el usuario es el dueño del historial
        series = self.db.query(series_pr_exercise).filter(series_pr_exercise.id == dropset_pr_exercise_data.serie_pr_exercise_id).first()
        if series:
            history = self.db.query(history_pr_exercise).filter(
                history_pr_exercise.id == series.history_pr_exercise_id,
                history_pr_exercise.user_email == user_email
            ).first()
            
            if not history:
                raise ValueError("No tienes permiso para crear dropsets en este historial")
                
        new_dropset = dropset_pr_exercise(
            serie_pr_exercise_id=dropset_pr_exercise_data.serie_pr_exercise_id,
            weight=dropset_pr_exercise_data.weight,
            reps=dropset_pr_exercise_data.reps
        )
        self.db.add(new_dropset)
        self.db.commit()
        self.db.refresh(new_dropset)
        return new_dropset
    
    def remove_dropset_pr_exercise(self, id: int, user_email: str) -> dict:
        """
        Elimina un dropset PR específico.
        """
        # Verificar que el usuario es el dueño del historial
        dropset = self.db.query(dropset_pr_exercise).filter(dropset_pr_exercise.id == id).first()
        if dropset:
            series = self.db.query(series_pr_exercise).filter(series_pr_exercise.id == dropset.serie_pr_exercise_id).first()
            if series:
                history = self.db.query(history_pr_exercise).filter(
                    history_pr_exercise.id == series.history_pr_exercise_id,
                    history_pr_exercise.user_email == user_email
                ).first()
                
                if not history:
                    raise ValueError("No tienes permiso para eliminar este dropset")
                    
            self.db.delete(dropset)
            self.db.commit()
        return dropset
    
    def get_dropset_pr_exercise_by_id(self, id: int) -> DropSetPrExercise:
        """
        Obtiene un dropset PR específico por su ID.
        """
        return self.db.query(dropset_pr_exercise).filter(dropset_pr_exercise.id == id).first()
    
    def update_dropset_pr_exercise(self, id: int, dropset_pr_exercise_data: DropSetPrExercise, user_email: str) -> DropSetPrExercise:
        """
        Actualiza un dropset PR específico.
        """
        # Verificar que el usuario es el dueño del historial
        dropset = self.db.query(dropset_pr_exercise).filter(dropset_pr_exercise.id == id).first()
        if dropset:
            series = self.db.query(series_pr_exercise).filter(series_pr_exercise.id == dropset.serie_pr_exercise_id).first()
            if series:
                history = self.db.query(history_pr_exercise).filter(
                    history_pr_exercise.id == series.history_pr_exercise_id,
                    history_pr_exercise.user_email == user_email
                ).first()
                
                if not history:
                    raise ValueError("No tienes permiso para actualizar este dropset")
                    
            dropset.weight = dropset_pr_exercise_data.weight
            dropset.reps = dropset_pr_exercise_data.reps
            dropset.orden_dropset = dropset_pr_exercise_data.orden_dropset
            self.db.commit()
            self.db.refresh(dropset)
        return dropset 