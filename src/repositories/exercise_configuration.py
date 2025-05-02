from typing import List
from src.schemas.exercise_configuration import ExerciseConfiguration
from src.models.exercise_configuration import ExerciseConfiguration as ExerciseConfigurationModel
from src.models.workout_day_exercise import WorkoutDayExercise as WorkoutDayExerciseModel
from src.models.training_plan import TrainingPlan as TrainingPlanModel
from src.models.user import User as UserModel
from src.repositories.user_gym import UserGymRepository

class ExerciseConfigurationRepository():
    def __init__(self, db) -> None:
        self.db = db
        self.user_gym_repo = UserGymRepository(db)
    
    def get_all_exercise_configurations(self) -> List[ExerciseConfiguration]:
        """
        Obtiene todos los ejercicios detallados.
        
        Precondición: Ninguna.
        Postcondición: Devuelve una lista de objetos ExerciseConfiguration que representan todos los ejercicios detallados en la base de datos.
        """
        query = self.db.query(ExerciseConfigurationModel)
        return query.all()
    
    def get_exercise_configuration_by_id(self, id: int, user_email: str = None):
        """
        Obtiene un ejercicio detallado por su ID.

        Parámetros:
        - id: el ID del ejercicio detallado que se desea obtener.
        - user_email: email del usuario que está solicitando la configuración (opcional)

        Precondición: El parámetro 'id' debe ser un entero válido.
        Postcondición: Devuelve un objeto ExerciseConfiguration que representa el ejercicio detallado con el ID especificado.
        """
        element = self.db.query(ExerciseConfigurationModel).filter(ExerciseConfigurationModel.id == id).first()
        
        # Si se proporciona user_email, verificar que el usuario tiene acceso a esta configuración
        if user_email and element:
            # Obtener el workout_day_exercise asociado
            workout_day_exercise = self.db.query(WorkoutDayExerciseModel).filter(
                WorkoutDayExerciseModel.id == element.workout_day_exercise_id
            ).first()
            
            if workout_day_exercise:
                # Obtener el plan de entrenamiento asociado
                training_plan = self.db.query(TrainingPlanModel).filter(
                    TrainingPlanModel.id == workout_day_exercise.training_plan_id
                ).first()
                
                # Si el usuario no es el dueño del plan de entrenamiento, no devolver la configuración
                if training_plan and training_plan.user_email != user_email:
                    return None
        
        return element
    
    def delete_exercise_configuration(self, id: int, user_email: str) -> dict:
        """
        Elimina un ejercicio detallado por su ID.

        Parámetros:
        - id: el ID del ejercicio detallado que se desea eliminar.
        - user_email: email del usuario que está eliminando la configuración
        
        Precondición: El parámetro 'id' debe ser un entero válido.
        Postcondición: Elimina el ejercicio detallado con el ID especificado de la base de datos y devuelve un diccionario que contiene los datos del ejercicio eliminado.
        """
        # Obtener el usuario actual
        current_user = self.db.query(UserModel).filter(UserModel.email == user_email).first()
        if not current_user:
            raise ValueError("Usuario no encontrado")

        # Obtener la configuración de ejercicio
        element = self.db.query(ExerciseConfigurationModel).filter(ExerciseConfigurationModel.id == id).first()
        if not element:
            raise ValueError(f"No existe una configuración de ejercicio con id {id}")

        # Obtener el workout day exercise
        workout_day_exercise = self.db.query(WorkoutDayExerciseModel).filter(
            WorkoutDayExerciseModel.id == element.workout_day_exercise_id
        ).first()
        if not workout_day_exercise:
            raise ValueError("Ejercicio por día de la semana no encontrado")

        # Obtener el plan de entrenamiento
        training_plan = self.db.query(TrainingPlanModel).filter(
            TrainingPlanModel.id == workout_day_exercise.training_plan_id
        ).first()
        if not training_plan:
            raise ValueError("Plan de entrenamiento no encontrado")

        # Obtener el usuario objetivo
        target_user = self.db.query(UserModel).filter(UserModel.email == training_plan.user_email).first()
        if not target_user:
            raise ValueError("Usuario objetivo no encontrado")

        # Verificar permisos
        can_delete = False

        # Si el usuario actual es administrador (role 4)
        if current_user.role_id == 4:
            can_delete = True
        # Si el usuario actual es el mismo que el objetivo y es premium (role 2)
        elif user_email == training_plan.user_email and current_user.role_id == 2:
            can_delete = True
        #Verifica que el plan fue creado por un gimnasio, que el gimnasio está asociado con el usuario (user_gym.is_active) y 
        #que ese mismo gimnasio fue el que creó el plan (training_plan.user_gym_id == user_gym.id).
        elif current_user.role_id == 3 and training_plan.is_gym_created:
            user_gym = self.user_gym_repo.get_user_gym(training_plan.user_email, user_email)
            if user_gym and user_gym.is_active and training_plan.user_gym_id == user_gym.id:
                can_create = True

        if not can_delete:
            raise ValueError("No tienes permiso para eliminar esta configuración de ejercicio")

        # Guardar los datos antes de eliminar
        element_data = element.to_dict()
        self.db.delete(element)
        self.db.commit()
        return element_data

    def create_new_exercise_configuration(self, exercise_configuration: ExerciseConfiguration, user_email: str) -> dict:
        """
        Crea un nuevo ejercicio detallado.

        Parámetros:
        - exercise_configuration: un objeto ExerciseConfiguration que contiene los datos del nuevo ejercicio a crear.
        - user_email: email del usuario que está creando la configuración
        
        Precondición: El parámetro 'exercise_configuration' debe ser un objeto ExerciseConfiguration válido.
        Postcondición: Crea un nuevo ejercicio detallado en la base de datos.
        """
        # Obtener el usuario actual
        current_user = self.db.query(UserModel).filter(UserModel.email == user_email).first()
        if not current_user:
            raise ValueError("Usuario no encontrado")

        # Verificar que el ejercicio por día de la semana existe
        workout_day_exercise = self.db.query(WorkoutDayExerciseModel).filter(
            WorkoutDayExerciseModel.id == exercise_configuration.workout_day_exercise_id
        ).first()
        if not workout_day_exercise:
            raise ValueError(f"El ejercicio por día de la semana con ID {exercise_configuration.workout_day_exercise_id} no existe")

        # Obtener el plan de entrenamiento
        training_plan = self.db.query(TrainingPlanModel).filter(
            TrainingPlanModel.id == workout_day_exercise.training_plan_id
        ).first()
        if not training_plan:
            raise ValueError("Plan de entrenamiento no encontrado")

        # Obtener el usuario objetivo
        target_user = self.db.query(UserModel).filter(UserModel.email == training_plan.user_email).first()
        if not target_user:
            raise ValueError("Usuario objetivo no encontrado")

        # Verificar permisos
        can_create = False

        # Si el usuario actual es administrador (role 4)
        if current_user.role_id == 4:
            can_create = True
        # Si el usuario actual es el mismo que el objetivo y es premium (role 2)
        elif user_email == training_plan.user_email and current_user.role_id == 2:
            can_create = True
        #Verifica que el plan fue creado por un gimnasio, que el gimnasio está asociado con el usuario (user_gym.is_active) y 
        #que ese mismo gimnasio fue el que creó el plan (training_plan.user_gym_id == user_gym.id).
        elif current_user.role_id == 3 and training_plan.is_gym_created:
            user_gym = self.user_gym_repo.get_user_gym(training_plan.user_email, user_email)
            if user_gym and user_gym.is_active and training_plan.user_gym_id == user_gym.id:
                can_create = True

        if not can_create:
            raise ValueError("No tienes permiso para crear configuraciones para este ejercicio")

        new_exercise_configuration = ExerciseConfigurationModel(**exercise_configuration.model_dump())
        self.db.add(new_exercise_configuration)
        self.db.commit()
        self.db.refresh(new_exercise_configuration)
        return new_exercise_configuration

    def update_exercise_configuration(self, id: int, exercise_configuration: ExerciseConfiguration, user_email: str) -> dict:
        """
        Actualiza un ejercicio detallado por su ID.

        Parámetros:
        - id: el ID del ejercicio detallado que se desea actualizar.
        - exercise_configuration: un objeto ExerciseConfiguration que contiene los datos actualizados del ejercicio detallado.
        - user_email: email del usuario que está actualizando la configuración
        
        Precondición: El parámetro 'id' debe ser un entero válido. El parámetro 'exercise_configuration' debe ser un objeto ExerciseConfiguration válido.
        Postcondición: Actualiza los datos del ejercicio detallado con el ID especificado utilizando los datos proporcionados en 'exercise_configuration' y devuelve un diccionario que contiene los datos del ejercicio actualizado.
        """
        # Obtener el usuario actual
        current_user = self.db.query(UserModel).filter(UserModel.email == user_email).first()
        if not current_user:
            raise ValueError("Usuario no encontrado")

        # Obtener la configuración de ejercicio existente
        element = self.db.query(ExerciseConfigurationModel).filter(ExerciseConfigurationModel.id == id).first()
        if not element:
            raise ValueError(f"No existe una configuración de ejercicio con id {id}")

        # Obtener el workout day exercise
        workout_day_exercise = self.db.query(WorkoutDayExerciseModel).filter(
            WorkoutDayExerciseModel.id == element.workout_day_exercise_id
        ).first()
        if not workout_day_exercise:
            raise ValueError("Ejercicio por día de la semana no encontrado")

        # Obtener el plan de entrenamiento
        training_plan = self.db.query(TrainingPlanModel).filter(
            TrainingPlanModel.id == workout_day_exercise.training_plan_id
        ).first()
        if not training_plan:
            raise ValueError("Plan de entrenamiento no encontrado")

        # Obtener el usuario objetivo
        target_user = self.db.query(UserModel).filter(UserModel.email == training_plan.user_email).first()
        if not target_user:
            raise ValueError("Usuario objetivo no encontrado")

        # Verificar permisos
        can_update = False

        # Si el usuario actual es administrador (role 4)
        if current_user.role_id == 4:
            can_update = True
        # Si el usuario actual es el mismo que el objetivo y es premium (role 2)
        elif user_email == training_plan.user_email and current_user.role_id == 2:
            can_update = True
        #Verifica que el plan fue creado por un gimnasio, que el gimnasio está asociado con el usuario (user_gym.is_active) y 
        #que ese mismo gimnasio fue el que creó el plan (training_plan.user_gym_id == user_gym.id).
        elif current_user.role_id == 3 and training_plan.is_gym_created:
            user_gym = self.user_gym_repo.get_user_gym(training_plan.user_email, user_email)
            if user_gym and user_gym.is_active and training_plan.user_gym_id == user_gym.id:
                can_create = True

        if not can_update:
            raise ValueError("No tienes permiso para actualizar esta configuración de ejercicio")

        element.exercise_id = exercise_configuration.exercise_id
        element.workout_day_exercise_id = exercise_configuration.workout_day_exercise_id
        element.sets = exercise_configuration.sets
        element.reps = exercise_configuration.reps
        element.rest = exercise_configuration.rest

        self.db.commit()
        self.db.refresh(element)
        return element
