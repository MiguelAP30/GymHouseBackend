from typing import List
from src.models.history_pr_exercise import HistoryPrExercise as history_pr_exercise
from src.schemas.history_pr_exercise import HistoryPrExercise

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
    
    def create_new_history_pr_exercise(self, history_pr_exercise_data: HistoryPrExercise) -> HistoryPrExercise:
        """
        Crea un nuevo historial de ejercicio PR.

        Args:
            history_pr_exercise_data: El objeto HistoryPrExercise que representa el historial de ejercicio PR a crear.

        Returns:
            El objeto HistoryPrExercise creado.

        Precondición:
            - history_pr_exercise_data debe ser un objeto HistoryPrExercise válido.

        Postcondición:
            - Se crea un nuevo historial de ejercicio PR.
        """
        # Crear el historial
        new_history = history_pr_exercise(
            user_email=history_pr_exercise_data.user_email,
            exercise_id=history_pr_exercise_data.exercise_id,
            date=history_pr_exercise_data.date
        )
        self.db.add(new_history)
        self.db.commit()
        self.db.refresh(new_history)
        return new_history
    
    def remove_history_pr_exercise(self, id: int) -> dict:
        """
        Elimina un historial de ejercicio PR específico.
        """
        element = self.db.query(history_pr_exercise).filter(history_pr_exercise.id == id).first()
        if element:
            self.db.delete(element)
            self.db.commit()
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
    
    def update_history_pr_exercise(self, id: int, history_pr_exercise_data: HistoryPrExercise) -> HistoryPrExercise:
        """
        Actualiza un historial de ejercicio PR específico.

        Precondición:
            - La base de datos debe estar conectada y disponible.
            - El ID debe ser un entero válido.
            - history_pr_exercise debe ser un objeto HistoryPrExercise válido.

        Postcondición:
            - Actualiza el historial de ejercicio PR con el ID especificado en la base de datos.
            - Devuelve un objeto HistoryPrExercise que representa el historial de ejercicio PR actualizado.
        """
        element = self.db.query(history_pr_exercise).filter(history_pr_exercise.id == id).first()
        if element:
            # Actualizar datos básicos del historial
            element.date = history_pr_exercise_data.date
            self.db.commit()
            self.db.refresh(element)
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
    
    def get_history_pr_exercise_by_user_id(self, user_email: str) -> List[HistoryPrExercise]:
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
    
    def get_history_pr_exercise_by_exercise_id_and_user_id(self, exercise_id: int, user_email: str) -> List[HistoryPrExercise]:
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
