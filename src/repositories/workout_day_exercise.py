from typing import List
from src.schemas.workout_day_exercise import WorkoutDayExercise
from src.models.workout_day_exercise import WorkoutDayExercise as WorkoutDayExerciseModel
from src.models.training_plan import TrainingPlan as TrainingPlanModel
from src.models.week_day import WeekDay as WeekDayModel
from src.models.exercise_configuration import ExerciseConfiguration as ExerciseConfigurationModel
from src.models.user import User as UserModel


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

    def get_premium_workout_day_exercises(self) -> List[WorkoutDayExercise]:
        """
        Obtiene todos los ejercicios por día de la semana para usuarios premium.

        Precondición:
        - Ninguna.

        Postcondición:
        - Devuelve una lista de ejercicios correspondientes a usuarios premium.
        """
        # Obtenemos los planes de entrenamiento de usuarios premium (role_id = 2)
        training_plans = self.db.query(TrainingPlanModel).\
            join(UserModel, TrainingPlanModel.user_email == UserModel.email).\
            filter(UserModel.role_id == 2).all()
        
        # Luego obtenemos los ejercicios por día de la semana para esos planes
        workout_day_exercises = []
        for training_plan in training_plans:
            exercises = self.db.query(WorkoutDayExerciseModel).\
                filter(WorkoutDayExerciseModel.training_plan_id == training_plan.id).all()
            workout_day_exercises.extend(exercises)
            
        return workout_day_exercises

    def get_gym_workout_day_exercises(self) -> List[WorkoutDayExercise]:
        """
        Obtiene todos los ejercicios por día de la semana para usuarios gimnasio.

        Precondición:
        - Ninguna.

        Postcondición:
        - Devuelve una lista de ejercicios correspondientes a usuarios gimnasio.
        """
        # Obtenemos los planes de entrenamiento de usuarios gimnasio (role_id = 3)
        training_plans = self.db.query(TrainingPlanModel).\
            join(UserModel, TrainingPlanModel.user_email == UserModel.email).\
            filter(UserModel.role_id == 3).all()
        
        # Luego obtenemos los ejercicios por día de la semana para esos planes
        workout_day_exercises = []
        for training_plan in training_plans:
            exercises = self.db.query(WorkoutDayExerciseModel).\
                filter(WorkoutDayExerciseModel.training_plan_id == training_plan.id).all()
            workout_day_exercises.extend(exercises)
            
        return workout_day_exercises

    def get_admin_workout_day_exercises(self) -> List[WorkoutDayExercise]:
        """
        Obtiene todos los ejercicios por día de la semana para usuarios administradores.

        Precondición:
        - Ninguna.

        Postcondición:
        - Devuelve una lista de ejercicios correspondientes a usuarios administradores.
        """
        # Obtenemos los planes de entrenamiento de usuarios administradores (role_id = 4)
        training_plans = self.db.query(TrainingPlanModel).\
            join(UserModel, TrainingPlanModel.user_email == UserModel.email).\
            filter(UserModel.role_id == 4).all()
        
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

    def create_new_workout_day_exercise(self, workout_day_exercise: WorkoutDayExercise) -> dict:
        """
        Crea un nuevo ejercicio por día de la semana.

        Parámetros:
        - workout_day_exercise: objeto WorkoutDayExercise que contiene los datos del ejercicio.

        Precondición:
        - Ninguna.

        Postcondición:
        - Crea un nuevo ejercicio por día de la semana en la base de datos y lo devuelve.
        """
        # Verificar que el training_plan_id existe
        training_plan = self.db.query(TrainingPlanModel).\
            filter(TrainingPlanModel.id == workout_day_exercise.training_plan_id).first()
        if not training_plan:
            raise ValueError(f"No existe un plan de entrenamiento con id {workout_day_exercise.training_plan_id}")
        
        # Verificar que el week_day_id existe
        week_day = self.db.query(WeekDayModel).\
            filter(WeekDayModel.id == workout_day_exercise.week_day_id).first()
        if not week_day:
            raise ValueError(f"No existe un día de la semana con id {workout_day_exercise.week_day_id}")
        
        # Verificar que el exercise_configuration_id existe si se proporciona
        if workout_day_exercise.exercise_configuration_id:
            exercise_configuration = self.db.query(ExerciseConfigurationModel).\
                filter(ExerciseConfigurationModel.id == workout_day_exercise.exercise_configuration_id).first()
            if not exercise_configuration:
                raise ValueError(f"No existe una configuración de ejercicio con id {workout_day_exercise.exercise_configuration_id}")
        
        new_workout_day_exercise = WorkoutDayExerciseModel(**workout_day_exercise.model_dump())
        self.db.add(new_workout_day_exercise)
        self.db.commit()
        self.db.refresh(new_workout_day_exercise)
        return new_workout_day_exercise

    def update_workout_day_exercise(self, id: int, workout_day_exercise: WorkoutDayExercise) -> dict:
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
        element = self.db.query(WorkoutDayExerciseModel).\
            filter(WorkoutDayExerciseModel.id == id).first()
        
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
        
        # Verificar que el exercise_configuration_id existe si se está actualizando
        if workout_day_exercise.exercise_configuration_id:
            exercise_configuration = self.db.query(ExerciseConfigurationModel).\
                filter(ExerciseConfigurationModel.id == workout_day_exercise.exercise_configuration_id).first()
            if not exercise_configuration:
                raise ValueError(f"No existe una configuración de ejercicio con id {workout_day_exercise.exercise_configuration_id}")
        
        element.training_plan_id = workout_day_exercise.training_plan_id
        element.week_day_id = workout_day_exercise.week_day_id
        element.exercise_configuration_id = workout_day_exercise.exercise_configuration_id
        
        self.db.commit()
        self.db.refresh(element)
        return element

    def delete_workout_day_exercise(self, id: int) -> dict:
        """
        Elimina un ejercicio por día de la semana.

        Parámetros:
        - id: ID del ejercicio.

        Precondición:
        - El ejercicio debe existir en la base de datos.

        Postcondición:
        - Elimina el ejercicio por día de la semana de la base de datos y lo devuelve.
        """
        element = self.db.query(WorkoutDayExerciseModel).\
            filter(WorkoutDayExerciseModel.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element