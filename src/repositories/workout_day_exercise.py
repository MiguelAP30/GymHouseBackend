from typing import List
from src.schemas.workout_day_exercise import WorkoutDayExercise
from src.models.workout_day_exercise import WorkoutDayExercise as WorkoutDayExerciseModel
from src.models.training_plan import TrainingPlan as TrainingPlanModel
from src.models.week_day import WeekDay as WeekDayModel
from src.models.exercise_configuration import ExerciseConfiguration as ExerciseConfigurationModel
from src.models.user import User as UserModel
from src.repositories.user_gym import UserGymRepository


class WorkoutDayExerciseRepository:
    def __init__(self, db) -> None:
        """
        Constructor de la clase WorkoutDayExerciseRepository.

        Parámetros:
        - db: objeto de la base de datos.

        Precondición:
        - Ninguna.

        Postcondición:
        - Se inicializa el objeto WorkoutDayExerciseRepository con la base de datos especificada.
        """
        self.db = db
        self.user_gym_repo = UserGymRepository(db)

    def get_all_workout_day_exercises(self) -> List[WorkoutDayExercise]:
        """
        Obtiene todos los ejercicios por día de la semana.

        Precondición:
        - Ninguna.

        Postcondición:
        - Devuelve una lista de todos los ejercicios por día de la semana.
        """
        query = self.db.query(WorkoutDayExerciseModel)
        return query.all()

    def get_all_my_workout_day_exercises(self, user_email: str) -> List[WorkoutDayExercise]:
        """
        Obtiene todos los ejercicios por día de la semana para un usuario específico.

        Parámetros:
        - user_email: Email del usuario.

        Precondición:
        - El usuario debe existir en la base de datos.

        Postcondición:
        - Devuelve una lista de ejercicios correspondientes al usuario proporcionado.
        """
        # Primero obtenemos los planes de entrenamiento del usuario
        training_plans = self.db.query(TrainingPlanModel).\
            filter(TrainingPlanModel.user_email == user_email).all()
        
        # Luego obtenemos los ejercicios por día de la semana para esos planes
        workout_day_exercises = []
        for training_plan in training_plans:
            exercises = self.db.query(WorkoutDayExerciseModel).\
                filter(WorkoutDayExerciseModel.training_plan_id == training_plan.id).all()
            workout_day_exercises.extend(exercises)
            
        return workout_day_exercises

    def get_workout_day_exercise_by_id(self, id: int) -> WorkoutDayExercise:
        """
        Obtiene un ejercicio por día de la semana y ID específicos.

        Parámetros:
        - id: ID del ejercicio.

        Precondición:
        - El ejercicio debe existir en la base de datos.

        Postcondición:
        - Devuelve el ejercicio correspondiente al ID proporcionado.
        """
        element = self.db.query(WorkoutDayExerciseModel).\
            filter(WorkoutDayExerciseModel.id == id).first()
        return element

    def get_workout_day_exercises_by_training_plan(self, training_plan_id: int) -> List[WorkoutDayExercise]:
        """
        Obtiene todos los ejercicios por día de la semana para un plan de entrenamiento específico.

        Parámetros:
        - training_plan_id: ID del plan de entrenamiento.

        Precondición:
        - El plan de entrenamiento debe existir en la base de datos.

        Postcondición:
        - Devuelve una lista de ejercicios correspondientes al plan de entrenamiento proporcionado.
        """
        query = self.db.query(WorkoutDayExerciseModel).\
            filter(WorkoutDayExerciseModel.training_plan_id == training_plan_id)
        return query.all()

    def get_workout_day_exercises_by_week_day(self, week_day_id: int) -> List[WorkoutDayExercise]:
        """
        Obtiene todos los ejercicios por día de la semana para un día específico de la semana.

        Parámetros:
        - week_day_id: ID del día de la semana.

        Precondición:
        - El día de la semana debe existir en la base de datos.

        Postcondición:
        - Devuelve una lista de ejercicios correspondientes al día de la semana proporcionado.
        """
        query = self.db.query(WorkoutDayExerciseModel).\
            filter(WorkoutDayExerciseModel.week_day_id == week_day_id)
        return query.all()

    def create_new_workout_day_exercise(self, workout_day_exercise: WorkoutDayExercise, user_email: str) -> dict:
        """
        Crea un nuevo ejercicio por día de la semana.

        Parámetros:
        - workout_day_exercise: objeto WorkoutDayExercise que contiene los datos del ejercicio.
        - user_email: email del usuario que está creando el workout day exercise

        Precondición:
        - Ninguna.

        Postcondición:
        - Crea un nuevo ejercicio por día de la semana en la base de datos y lo devuelve.
        """
        # Obtener el usuario actual
        current_user = self.db.query(UserModel).filter(UserModel.email == user_email).first()
        if not current_user:
            raise ValueError("Usuario no encontrado")

        # Obtener el plan de entrenamiento
        training_plan = self.db.query(TrainingPlanModel).\
            filter(TrainingPlanModel.id == workout_day_exercise.training_plan_id).first()
        if not training_plan:
            raise ValueError(f"No existe un plan de entrenamiento con id {workout_day_exercise.training_plan_id}")

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
        # Si el usuario actual es un gimnasio (role 3) y el objetivo es premium (role 2)
        elif current_user.role_id == 3 and target_user.role_id == 2:
            # Verificar que el gimnasio puede gestionar el plan del usuario
            user_gym = self.user_gym_repo.get_user_gym(target_user.email, user_email)
            if user_gym and user_gym.is_active:
                can_create = True

        if not can_create:
            raise ValueError("No tienes permiso para crear ejercicios para este plan de entrenamiento")

        # Verificar que el week_day_id existe
        week_day = self.db.query(WeekDayModel).\
            filter(WeekDayModel.id == workout_day_exercise.week_day_id).first()
        if not week_day:
            raise ValueError(f"No existe un día de la semana con id {workout_day_exercise.week_day_id}")
        
        # Verificar si ya existe un workout day exercise con el mismo training_plan_id y week_day_id
        existing_workout = self.db.query(WorkoutDayExerciseModel).\
            filter(
                WorkoutDayExerciseModel.training_plan_id == workout_day_exercise.training_plan_id,
                WorkoutDayExerciseModel.week_day_id == workout_day_exercise.week_day_id
            ).first()
        
        if existing_workout:
            raise ValueError(f"Ya existe un ejercicio para el día {workout_day_exercise.week_day_id} en el plan de entrenamiento {workout_day_exercise.training_plan_id}")
        
        new_workout_day_exercise = WorkoutDayExerciseModel(**workout_day_exercise.model_dump())
        self.db.add(new_workout_day_exercise)
        self.db.commit()
        self.db.refresh(new_workout_day_exercise)
        return new_workout_day_exercise

    def update_workout_day_exercise(self, id: int, workout_day_exercise: WorkoutDayExercise, user_email: str) -> dict:
        """
        Actualiza un ejercicio por día de la semana.

        Parámetros:
        - id: ID del ejercicio.
        - workout_day_exercise: objeto WorkoutDayExercise que contiene los datos actualizados del ejercicio.

        Precondición:
        - El ejercicio y el ID deben existir en la base de datos.

        Postcondición:
        - Actualiza el ejercicio por día de la semana en la base de datos y lo devuelve.
        """
        # Obtener el usuario actual
        current_user = self.db.query(UserModel).filter(UserModel.email == user_email).first()
        if not current_user:
            raise ValueError("Usuario no encontrado")

        # Obtener el workout day exercise existente
        element = self.db.query(WorkoutDayExerciseModel).\
            filter(WorkoutDayExerciseModel.id == id).first()
        if not element:
            raise ValueError(f"No existe un ejercicio con id {id}")

        # Obtener el plan de entrenamiento
        training_plan = self.db.query(TrainingPlanModel).\
            filter(TrainingPlanModel.id == element.training_plan_id).first()
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
        # Si el usuario actual es un gimnasio (role 3) y el objetivo es premium (role 2)
        elif current_user.role_id == 3 and target_user.role_id == 2:
            # Verificar que el gimnasio puede gestionar el plan del usuario
            user_gym = self.user_gym_repo.get_user_gym(target_user.email, user_email)
            if user_gym and user_gym.is_active:
                can_update = True

        if not can_update:
            raise ValueError("No tienes permiso para actualizar este ejercicio")

        # Verificar que el training_plan_id existe si se está actualizando
        if workout_day_exercise.training_plan_id:
            training_plan = self.db.query(TrainingPlanModel).\
                filter(TrainingPlanModel.id == workout_day_exercise.training_plan_id).first()
            if not training_plan:
                raise ValueError(f"No existe un plan de entrenamiento con id {workout_day_exercise.training_plan_id}")
        
        # Verificar que el week_day_id existe si se está actualizando
        if workout_day_exercise.week_day_id:
            week_day = self.db.query(WeekDayModel).\
                filter(WeekDayModel.id == workout_day_exercise.week_day_id).first()
            if not week_day:
                raise ValueError(f"No existe un día de la semana con id {workout_day_exercise.week_day_id}")
        
        element.training_plan_id = workout_day_exercise.training_plan_id
        element.week_day_id = workout_day_exercise.week_day_id
        
        self.db.commit()
        self.db.refresh(element)
        return element

    def delete_workout_day_exercise(self, id: int, user_email: str) -> dict:
        """
        Elimina un ejercicio por día de la semana.

        Parámetros:
        - id: ID del ejercicio.

        Precondición:
        - El ejercicio debe existir en la base de datos.

        Postcondición:
        - Elimina el ejercicio por día de la semana de la base de datos y lo devuelve.
        """
        # Obtener el usuario actual
        current_user = self.db.query(UserModel).filter(UserModel.email == user_email).first()
        if not current_user:
            raise ValueError("Usuario no encontrado")

        # Obtener el workout day exercise
        element = self.db.query(WorkoutDayExerciseModel).\
            filter(WorkoutDayExerciseModel.id == id).first()
        if not element:
            raise ValueError(f"No existe un ejercicio con id {id}")

        # Obtener el plan de entrenamiento
        training_plan = self.db.query(TrainingPlanModel).\
            filter(TrainingPlanModel.id == element.training_plan_id).first()
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
        # Si el usuario actual es un gimnasio (role 3) y el objetivo es premium (role 2)
        elif current_user.role_id == 3 and target_user.role_id == 2:
            # Verificar que el gimnasio puede gestionar el plan del usuario
            user_gym = self.user_gym_repo.get_user_gym(target_user.email, user_email)
            if user_gym and user_gym.is_active:
                can_delete = True

        if not can_delete:
            raise ValueError("No tienes permiso para eliminar este ejercicio")

        # Eliminar las configuraciones de ejercicios asociadas
        self.db.query(ExerciseConfigurationModel).\
            filter(ExerciseConfigurationModel.workout_day_exercise_id == id).delete()

        # Eliminar el workout day exercise
        self.db.delete(element)
        self.db.commit()
        return element