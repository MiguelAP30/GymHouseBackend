from typing import List
from src.schemas.detailed_exercise import DetailedExercise
from src.models.detailed_exercise import DetailedExercise as detailed_exercises

class DetailedExerciseRepository():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all_detailed_exercise(self) -> List[DetailedExercise]:
        """
        Obtiene todos los ejercicios detallados.
        
        Precondición: Ninguna.
        Postcondición: Devuelve una lista de objetos DetailedExercise que representan todos los ejercicios detallados en la base de datos.
        """
        query = self.db.query(detailed_exercises)
        return query.all()
    
    def get_detailed_exercise_by_id(self, id: int ):
        """
        Obtiene un ejercicio detallado por su ID.

        Parámetros:
        - id: el ID del ejercicio detallado que se desea obtener.

        Precondición: El parámetro 'id' debe ser un entero válido.
        Postcondición: Devuelve un objeto DetailedExercise que representa el ejercicio detallado con el ID especificado.
        """
        element = self.db.query(detailed_exercises).filter(detailed_exercises.id == id).first()
        return element
    
    def delete_detailed_exercise(self, id: int ) -> dict:
        """
        Elimina un ejercicio detallado por su ID.

        Parámetros:
        - id: el ID del ejercicio detallado que se desea eliminar.
        
        Precondición: El parámetro 'id' debe ser un entero válido.
        Postcondición: Elimina el ejercicio detallado con el ID especificado de la base de datos y devuelve un diccionario que contiene los datos del ejercicio eliminado.
        """
        element: DetailedExercise= self.db.query(detailed_exercises).filter(detailed_exercises.id == id).first()
        self.db.delete(element)

        self.db.commit()
        self.db.refresh(element)
        return element

    def create_new_detailed_exercise(self, detailed_exercise:DetailedExercise ) -> dict:
        """
        Crea un nuevo ejercicio detallado.

        Parámetros:
        - detailed_exercise: un objeto DetailedExercise que contiene los datos del nuevo ejercicio a crear.
        
        Precondición: El parámetro 'detailed_exercise' debe ser un objeto DetailedExercise válido.
        Postcondición: Crea un nuevo ejercicio detallado en la base de datos utilizando los datos proporcionados en 'detailed_exercise' y devuelve un diccionario que contiene los datos del nuevo ejercicio creado.
        """
        new_detailed_exercise = detailed_exercises(**detailed_exercise.model_dump())
        self.db.add(new_detailed_exercise)
        
        self.db.commit()
        self.db.refresh(new_detailed_exercise)
        return new_detailed_exercise

    def update_detailed_exercise(self, id: int, detailed_exercise: DetailedExercise) -> dict:
        """
        Actualiza un ejercicio detallado por su ID.

        Parámetros:
        - id: el ID del ejercicio detallado que se desea actualizar.
        - detailed_exercise: un objeto DetailedExercise que contiene los datos actualizados del ejercicio detallado.
        
        Precondición: El parámetro 'id' debe ser un entero válido. El parámetro 'detailed_exercise' debe ser un objeto DetailedExercise válido.
        Postcondición: Actualiza los datos del ejercicio detallado con el ID especificado utilizando los datos proporcionados en 'detailed_exercise' y devuelve un diccionario que contiene los datos del ejercicio actualizado.
        """
        element: DetailedExercise = self.db.query(detailed_exercises).filter(detailed_exercises.id == id).first()
        element.sets = detailed_exercise.sets
        element.reps = detailed_exercise.reps
        element.rest = detailed_exercise.rest

        self.db.commit()
        self.db.refresh(element)
        return element
