from typing import List
from src.models.history_pr_exercise import HistoryPrExercise as history_pr_exercise
from src.schemas.history_pr_exercise import HistoryPrExercise, HistoryPrExerciseUpdate, FullHistoryPrExerciseCreate
from src.models.series_pr_exercise import SeriesPrExercise as series_pr_exercise
from src.models.dropset_pr_exercise import DropSetPrExercise as dropset_pr_exercise


class HistoryPrExerciseRepository():
    def __init__(self, db) -> None:
        """
        Inicializa una nueva instancia de la clase HistoryPrExerciseRepository.

        Args:
            db: La base de datos utilizada para realizar las operaciones.

        Precondición:
            - db debe ser una instancia válida de la base de datos.

        Postcondición:
            - Se crea una nueva instancia de HistoryPrExerciseRepository.
        """
        self.db = db
    
    def get_all_history_pr_exercise(self, user_email: str) -> List[HistoryPrExercise]:
        """
        Obtiene todos los historiales de ejercicios PR del usuario.

        Returns:
            Una lista de objetos HistoryPrExercise que representan los historiales de ejercicios PR.

        Postcondición:
            - Se devuelve una lista de objetos HistoryPrExercise.
        """
        query = self.db.query(history_pr_exercise).filter(history_pr_exercise.user_email == user_email)
        return query.all()
    
    def create_new_history_pr_exercise(self, user_email: str, full_data: FullHistoryPrExerciseCreate) -> dict:
        try:
            # Crear el historial principal
            new_history = history_pr_exercise(
                user_email=user_email,
                exercise_id=full_data.exercise_id,
                date=full_data.date,
                notas=full_data.notas,
                tipo_sesion=full_data.tipo_sesion
            )
            self.db.add(new_history)
            self.db.commit()
            self.db.refresh(new_history)

            all_series = []

            # Crear series y dropsets
            for serie in full_data.series:
                new_serie = series_pr_exercise(
                    history_pr_exercise_id=new_history.id,
                    weight=serie.weight,
                    reps=serie.reps,
                    tipo_serie=serie.tipo_serie,
                    rpe=serie.rpe,
                    orden_serie=serie.orden_serie,
                    notas_serie=serie.notas_serie
                )
                self.db.add(new_serie)
                self.db.commit()
                self.db.refresh(new_serie)

                all_dropsets = []

                for dropset in serie.dropsets:
                    new_dropset = dropset_pr_exercise(
                        serie_pr_exercise_id=new_serie.id,
                        weight=dropset.weight,
                        reps=dropset.reps,
                        orden_dropset=dropset.orden_dropset
                    )
                    self.db.add(new_dropset)
                    self.db.commit()
                    self.db.refresh(new_dropset)
                    all_dropsets.append({
                        "id": new_dropset.id,
                        "weight": new_dropset.weight,
                        "reps": new_dropset.reps,
                        "orden_dropset": new_dropset.orden_dropset
                    })

                all_series.append({
                    "id": new_serie.id,
                    "weight": new_serie.weight,
                    "reps": new_serie.reps,
                    "tipo_serie": new_serie.tipo_serie,
                    "rpe": new_serie.rpe,
                    "orden_serie": new_serie.orden_serie,
                    "notas_serie": new_serie.notas_serie,
                    "dropsets": all_dropsets
                })

            return {
                "id": new_history.id,
                "user_email": new_history.user_email,
                "exercise_id": new_history.exercise_id,
                "date": str(new_history.date),
                "notas": new_history.notas,
                "tipo_sesion": new_history.tipo_sesion,
                "series": all_series
            }

        except Exception as e:
            self.db.rollback()
            raise e
    
    def remove_history_pr_exercise(self, id: int, user_email: str) -> dict:
        element = self.db.query(history_pr_exercise).filter(history_pr_exercise.id == id).first()
        if not element:
            raise ValueError("Historial no encontrado")

        if element.user_email != user_email:
            raise PermissionError("No tienes permiso para eliminar este historial")

        self.db.delete(element)
        self.db.commit()
        return {"message": "Historial eliminado correctamente"}
    
    def update_history_pr_exercise(self, id: int, history_pr_exercise_data: HistoryPrExerciseUpdate, user_email: str) -> history_pr_exercise:
        element = self.db.query(history_pr_exercise).filter(history_pr_exercise.id == id).first()
        if not element:
            raise ValueError("Historial no encontrado")

        if element.user_email != user_email:
            raise PermissionError("No tienes permiso para editar este historial")

        for field, value in history_pr_exercise_data.model_dump(exclude_unset=True).items():
            setattr(element, field, value)

        self.db.commit()
        self.db.refresh(element)
        return element

    
    def get_history_pr_exercise_by_id(self, id: int, user_email: str) -> HistoryPrExercise:
        """
        Obtiene un historial de ejercicio PR específico por su ID.

        Precondición:
            - La base de datos debe estar conectada y disponible.
            - El ID debe ser un entero válido.

        Postcondición:
            - Devuelve un objeto HistoryPrExercise que representa el historial de ejercicio PR con el ID especificado.
        """
        element = self.db.query(history_pr_exercise).filter(
            history_pr_exercise.id == id,
            history_pr_exercise.user_email == user_email
        ).first()
        return element
    
    
    def get_history_pr_exercise_by_exercise_id(self, exercise_id: int, user_email: str) -> List[HistoryPrExercise]:
        """
        Obtiene todos los historiales de ejercicio PR de un ejercicio específico.

        Precondición:
            - La base de datos debe estar conectada y disponible.
            - El ID debe ser un entero válido.

        Postcondición:
            - Devuelve una lista de objetos HistoryPrExercise que representa los historiales de ejercicio PR del ejercicio especificado.
        """
        elements = self.db.query(history_pr_exercise).filter(
            history_pr_exercise.exercise_id == exercise_id,
            history_pr_exercise.user_email == user_email
        ).all()
        return elements
    
    def get_history_pr_exercise_by_user_email(self, user_email: str) -> List[HistoryPrExercise]:
        """
        Obtiene todos los historiales de ejercicio PR de un usuario específico.

        Precondición:
            - La base de datos debe estar conectada y disponible.
            - El email debe ser un string válido.

        Postcondición:
            - Devuelve una lista de objetos HistoryPrExercise que representa los historiales de ejercicio PR del usuario especificado.
        """
        elements = self.db.query(history_pr_exercise).filter(history_pr_exercise.user_email == user_email).all()
        return elements
    
    def get_history_pr_exercise_by_exercise_id_and_user_email(self, exercise_id: int, user_email: str) -> List[HistoryPrExercise]:
        """
        Obtiene todos los historiales de ejercicio PR de un ejercicio y usuario específicos.

        Precondición:
            - La base de datos debe estar conectada y disponible.
            - El ID debe ser un entero válido.
            - El email debe ser un string válido.

        Postcondición:
            - Devuelve una lista de objetos HistoryPrExercise que representa los historiales de ejercicio PR del ejercicio y usuario especificados.
        """
        elements = self.db.query(history_pr_exercise).filter(
            history_pr_exercise.exercise_id == exercise_id,
            history_pr_exercise.user_email == user_email
        ).all()
        return elements
