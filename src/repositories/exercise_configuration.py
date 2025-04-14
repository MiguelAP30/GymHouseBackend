from typing import List
from src.schemas.exercise_configuration import ExerciseConfiguration
from src.models.exercise_configuration import ExerciseConfiguration as ExerciseConfigurationModel
from src.models.workout_day_exercise import WorkoutDayExercise as WorkoutDayExerciseModel

class ExerciseConfigurationRepository():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all_exercise_configurations(self) -> List[ExerciseConfiguration]:
        """
        Obtiene todos los ejercicios detallados.
        
        Precondición: Ninguna.
        Postcondición: Devuelve una lista de objetos ExerciseConfiguration que representan todos los ejercicios detallados en la base de datos.
        """
        query = self.db.query(ExerciseConfigurationModel)
        return query.all()
    
    def get_exercise_configuration_by_id(self, id: int ):
        """
        Obtiene un ejercicio detallado por su ID.

        Parámetros:
        - id: el ID del ejercicio detallado que se desea obtener.

        Precondición: El parámetro 'id' debe ser un entero válido.
        Postcondición: Devuelve un objeto ExerciseConfiguration que representa el ejercicio detallado con el ID especificado.
        """
        element = self.db.query(ExerciseConfigurationModel).filter(ExerciseConfigurationModel.id == id).first()
        return element
    
    def delete_exercise_configuration(self, id: int ) -> dict:
        """
        Elimina un ejercicio detallado por su ID.

        Parámetros:
        - id: el ID del ejercicio detallado que se desea eliminar.
        
        Precondición: El parámetro 'id' debe ser un entero válido.
        Postcondición: Elimina el ejercicio detallado con el ID especificado de la base de datos y devuelve un diccionario que contiene los datos del ejercicio eliminado.
        """
        element: ExerciseConfiguration= self.db.query(ExerciseConfigurationModel).filter(ExerciseConfigurationModel.id == id).first()
        self.db.delete(element)

        self.db.commit()
        self.db.refresh(element)
        return element

    def create_new_exercise_configuration(self, exercise_configuration:ExerciseConfiguration) -> dict:
        """
        Crea un nuevo ejercicio detallado.

        Parámetros:
        - exercise_configuration: un objeto ExerciseConfiguration que contiene los datos del nuevo ejercicio a crear.
        
        Precondición: El parámetro 'exercise_configuration' debe ser un objeto ExerciseConfiguration válido.
        Postcondición: Crea un nuevo ejercicio detallado en la base de datos.
        """
        # Verificar que el ejercicio por día de la semana existe
        workout_day_exercise = self.db.query(WorkoutDayExerciseModel).filter(
            WorkoutDayExerciseModel.id == exercise_configuration.workout_day_exercise_id
        ).first()
        
        if not workout_day_exercise:
            raise ValueError(f"El ejercicio por día de la semana con ID {exercise_configuration.workout_day_exercise_id} no existe")
        
        new_exercise_configuration = ExerciseConfigurationModel(**exercise_configuration.model_dump())
        self.db.add(new_exercise_configuration)
        self.db.commit()
        self.db.refresh(new_exercise_configuration)
        return new_exercise_configuration

    def update_exercise_configuration(self, id: int, exercise_configuration: ExerciseConfiguration) -> dict:
        """
        Actualiza un ejercicio detallado por su ID.

        Parámetros:
        - id: el ID del ejercicio detallado que se desea actualizar.
        - exercise_configuration: un objeto ExerciseConfiguration que contiene los datos actualizados del ejercicio detallado.
        
        Precondición: El parámetro 'id' debe ser un entero válido. El parámetro 'exercise_configuration' debe ser un objeto ExerciseConfiguration válido.
        Postcondición: Actualiza los datos del ejercicio detallado con el ID especificado utilizando los datos proporcionados en 'exercise_configuration' y devuelve un diccionario que contiene los datos del ejercicio actualizado.
        """
        element: ExerciseConfiguration = self.db.query(ExerciseConfigurationModel).filter(ExerciseConfigurationModel.id == id).first()
        element.exercise_id = exercise_configuration.exercise_id
        element.workout_day_exercise_id = exercise_configuration.workout_day_exercise_id
        element.sets = exercise_configuration.sets
        element.reps = exercise_configuration.reps
        element.rest = exercise_configuration.rest

        self.db.commit()
        self.db.refresh(element)
        return element
