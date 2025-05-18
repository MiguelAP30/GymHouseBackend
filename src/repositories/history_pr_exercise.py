from typing import List
from src.models.history_pr_exercise import HistoryPrExercise as history_pr_exercise
from src.schemas.history_pr_exercise import HistoryPrExercise, HistoryPrExerciseUpdate


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
        new_history = history_pr_exercise(**history_pr_exercise_data.model_dump())
        self.db.add(new_history)
        self.db.commit()
        self.db.refresh(new_history)
        return new_history
    
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
