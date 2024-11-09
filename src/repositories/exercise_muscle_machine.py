from typing import List

from sqlalchemy import desc
from src.schemas.exercise_muscle import ExerciseMuscle
from models.exercise_muscle import ExerciseMuscle as ExcersiceMuscleMachineModel
from src.models.muscle import Muscle as MuscleModel
from src.models.machine import Machine as MachineModel



class ExerciseMuscleMachineRepository():
    def __init__(self, db) -> None:
        self.db = db

    def get_all_excercise_muscle_by_rate(self, muscle: int) -> List[ExerciseMuscle]: 
        """
        Obtiene todos los ejercicios de un músculo específico ordenados por tasa de calificación.

        Parámetros:
        - muscle: el ID del músculo del cual se desean obtener los ejercicios.

        Precondición:
        - muscle: el ID del músculo del cual se desean obtener los ejercicios.

        Postcondición:
        - Devuelve una lista de objetos ExerciseMuscleMachine ordenados por tasa de calificación descendente.
        """

        query = self.db.query(ExcersiceMuscleMachineModel).join(MuscleModel).filter(MuscleModel.id == muscle).order_by(desc(ExcersiceMuscleMachineModel.rate))
        return query.all()

    def get_all_excercise_muscle_machine_by_rate(self, muscle: int, machine: int) -> List[ExerciseMuscle]:
        """
        Obtiene todos los ejercicios de un músculo y una máquina específicos ordenados por tasa de calificación.

        Parámetros:
        - muscle: el ID del músculo del cual se desean obtener los ejercicios.
        - machine: el ID de la máquina en la cual se desean obtener los ejercicios.

        Precondición:
        - muscle: el ID del músculo del cual se desean obtener los ejercicios.
        - machine: el ID de la máquina en la cual se desean obtener los ejercicios.

        Postcondición:
        - Devuelve una lista de objetos ExerciseMuscleMachine ordenados por tasa de calificación descendente.
        """

        query = self.db.query(ExcersiceMuscleMachineModel).join(MuscleModel).join(MachineModel).filter(MuscleModel.id == muscle, MachineModel.id == machine).order_by(desc(ExcersiceMuscleMachineModel.rate))
        return query.all()

    def get_excercise_muscle_machine_by_id(self, id: int ):
        """
        Obtiene un ejercicio de músculo y máquina específico por su ID.

        parámetros:
        - id: el ID del ExerciseMuscleMachine que se desea obtener.

        Precondición:
        - id: el ID del ExerciseMuscleMachine que se desea obtener.

        Postcondición:
        - Devuelve el objeto ExerciseMuscleMachine correspondiente al ID proporcionado.
        """

        element = self.db.query(ExcersiceMuscleMachineModel).filter(ExcersiceMuscleMachineModel.id == id).first()    
        return element

    def delete_excercise_muscle_machine(self, id: int) -> dict: 
        """
        Elimina un ejercicio de músculo y máquina específico por su ID.

        parámetros:
        - id: el ID del ExerciseMuscleMachine que se desea eliminar.

        Precondición:
        - id: el ID del ExerciseMuscleMachine que se desea eliminar.

        Postcondición:
        - Devuelve un diccionario que contiene los datos del ExerciseMuscleMachine eliminado.
        """

        element: ExerciseMuscle = self.db.query(ExcersiceMuscleMachineModel).filter(ExcersiceMuscleMachineModel.id == id).first()       
        self.db.delete(element)    
        self.db.commit()    
        return element

    def create_new_excercise_muscle_machine(self, excercise: ExerciseMuscle ) -> dict:
        """
        Crea un nuevo ejercicio de músculo y máquina.

        Parámetros:
        - excercise: el objeto ExerciseMuscleMachine que se desea crear.

        Precondición:
        - excercise: el objeto ExerciseMuscleMachine que se desea crear.

        Postcondición:
        - Devuelve un diccionario que contiene los datos del ExerciseMuscleMachine creado.
        """

        new_excercise = ExcersiceMuscleMachineModel(**excercise.model_dump())    
        
        self.db.add(new_excercise)
        self.db.commit()    
        self.db.refresh(new_excercise)
        return new_excercise

    def update_rate_excercise_muscle_machine(self, id: int, excercise: ExerciseMuscle) -> dict:
        """
        Actualiza la tasa de calificación de un ejercicio de músculo y máquina específico.

        Parámetros:
        - id: el ID del ExerciseMuscleMachine que se desea actualizar.
        - excercise: el objeto ExerciseMuscleMachine que contiene la nueva tasa de calificación.

        Precondición:
        - id: el ID del ExerciseMuscleMachine que se desea actualizar.
        - excercise: el objeto ExerciseMuscleMachine que contiene la nueva tasa de calificación.

        Postcondición:
        - Devuelve un diccionario que contiene los datos del ejercicio actualizado.
        """

        element = self.db.query(ExcersiceMuscleMachineModel).filter(ExcersiceMuscleMachineModel.id == id).first()
        element.rate = excercise.rate

        self.db.commit()
        self.db.refresh(element)
        return element
