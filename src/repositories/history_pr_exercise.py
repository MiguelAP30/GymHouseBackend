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
    
    def get_all_history_pr_exercise(self) -> List[HistoryPrExercise]:
        """
        Obtiene todos los historiales de ejercicios PR.

        Returns:
            Una lista de objetos HistoryPrExercise que representan los historiales de ejercicios PR.

        Postcondición:
            - Se devuelve una lista de objetos HistoryPrExercise.
        """
        query = self.db.query(history_pr_exercise)
        return query.all()
    
    def create_new_history_pr_exercise(self, history_pr_exercise: HistoryPrExercise) -> HistoryPrExercise:
        """
        Crea un nuevo historial de ejercicio PR.

        Args:
            history_pr_exercise: El objeto HistoryPrExercise que representa el historial de ejercicio PR a crear.

        Returns:
            El objeto HistoryPrExercise creado.

        Precondición:
            - history_pr_exercise debe ser un objeto HistoryPrExercise válido.

        Postcondición:
            - Se crea un nuevo historial de ejercicio PR.
        """

        new_history_pr_exercise = history_pr_exercise(**history_pr_exercise.model_dump())
        self.db.add(new_history_pr_exercise)

        self.db.commit()
        self.db.refresh(new_history_pr_exercise)
        return new_history_pr_exercise
    
    def remove_history_pr_exercise(self, id: int) -> dict:
        """
        Elimina un historial de ejercicio PR específico.
        """
        element: HistoryPrExercise = self.db.query(history_pr_exercise).filter(history_pr_exercise.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element
    
    def get_history_pr_exercise_by_id(self, id: int) -> HistoryPrExercise:
        """
        Obtiene un historial de ejercicio PR específico por su ID.

        Precondición:
            - La base de datos debe estar conectada y disponible.
            - El ID debe ser un entero válido.

        Postcondición:
            - Devuelve un objeto HistoryPrExercise que representa el historial de ejercicio PR con el ID especificado.
        """
        element = self.db.query(history_pr_exercise).filter(history_pr_exercise.id == id).first()
        return element
    
    def update_history_pr_exercise(self, id: int, history_pr_exercise: HistoryPrExercise) -> HistoryPrExercise:
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
        element.name = history_pr_exercise.name
        element.description = history_pr_exercise.description
        self.db.commit()
        self.db.refresh(element)
        return element
    
    def get_history_pr_exercise_by_exercise_id(self, exercise_id: int) -> HistoryPrExercise:
        """
        Obtiene un historial de ejercicio PR específico por su ID de ejercicio.

        Precondición:
            - La base de datos debe estar conectada y disponible.
            - El ID debe ser un entero válido.

        Postcondición:
            - Devuelve un objeto HistoryPrExercise que representa el historial de ejercicio PR con el ID de ejercicio especificado.
        """
        element = self.db.query(history_pr_exercise).filter(history_pr_exercise.exercise_id == exercise_id).first()
        return element
    
    def get_history_pr_exercise_by_user_id(self, user_id: int) -> HistoryPrExercise:
        """
        Obtiene un historial de ejercicio PR específico por su ID de usuario.

        Precondición:
            - La base de datos debe estar conectada y disponible.
            - El ID debe ser un entero válido.

        Postcondición:
            - Devuelve un objeto HistoryPrExercise que representa el historial de ejercicio PR con el ID de usuario especificado.
        """
        element = self.db.query(history_pr_exercise).filter(history_pr_exercise.user_id == user_id).first()
        return element
    
    def get_history_pr_exercise_by_exercise_id_and_user_id(self, exercise_id: int, user_id: int) -> HistoryPrExercise:
        """
        Obtiene un historial de ejercicio PR específico por su ID de ejercicio y usuario.

        Precondición:
            - La base de datos debe estar conectada y disponible.
            - El ID debe ser un entero válido.

        Postcondición:
            - Devuelve un objeto HistoryPrExercise que representa el historial de ejercicio PR con el ID de ejercicio y usuario especificado.
        """
        element = self.db.query(history_pr_exercise).filter(history_pr_exercise.exercise_id == exercise_id).filter(history_pr_exercise.user_id == user_id).first()
        return element
