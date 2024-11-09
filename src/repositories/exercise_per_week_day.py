from typing import List
from src.models.exercise_per_week_day import ExercisePerWeekDay as ExercisePerWeekDayModel
from src.models.week_day import WeekDay as WeekDayModel
from src.models.training_plan import TrainingPlan as TrainingPlanModel
from src.models.user import User as UserModel
from src.schemas.exercise_per_week_day import ExercisePerWeekDay


class ExercisePerWeekDayRepository:
    def __init__(self, db):
        """
        Constructor de la clase ExercisePerWeekDayRepository.

        Parámetros:
        - db: objeto de la base de datos.

        Precondición:
        - Ninguna.

        Postcondición:
        - Se inicializa el objeto ExercisePerWeekDayRepository con la base de datos especificada.
        """
        self.db = db

    def get_all_my_excercise_per_week_day(self, user: str):
        """
        Obtiene todos los ejercicios por día de la semana para un usuario específico.

        Parámetros:
        - user: correo electrónico del usuario.

        Precondición:
        - El usuario debe existir en la base de datos.

        Postcondición:
        - Devuelve un diccionario que agrupa los ejercicios por día de la semana y plan de entrenamiento.
        """
        exercises = self.db.query(ExercisePerWeekDayModel, WeekDayModel.name, TrainingPlanModel.name, UserModel.name).\
        select_from(ExercisePerWeekDayModel).\
        join(TrainingPlanModel).\
        join(WeekDayModel, ExercisePerWeekDayModel.week_day_id == WeekDayModel.id).\
        filter(TrainingPlanModel.user_email == user).\
        all()

        return self.group_exercises_by_day_and_training_plan(exercises)

    def get_premium_excercise_per_week_day(self):
        """
        Obtiene todos los ejercicios por día de la semana para usuarios premium.

        Precondición:
        - Ninguna.

        Postcondición:
        - Devuelve un diccionario que agrupa los ejercicios por día de la semana y plan de entrenamiento.
        """
        exercises = self.db.query(ExercisePerWeekDayModel, WeekDayModel.name, TrainingPlanModel.name, UserModel.name).\
            select_from(ExercisePerWeekDayModel).\
            join(TrainingPlanModel).\
            filter(TrainingPlanModel.is_visible == True).\
            join(UserModel).\
            filter(UserModel.role_id == 2).\
            join(WeekDayModel, ExercisePerWeekDayModel.week_day_id == WeekDayModel.id).\
            all()

        return self.group_exercises_by_day_and_training_plan(exercises)

    def get_client_excercise_per_week_day(self):
        """
        Obtiene todos los ejercicios por día de la semana para usuarios clientes.

        Precondición:
        - Ninguna.

        Postcondición:
        - Devuelve un diccionario que agrupa los ejercicios por día de la semana y plan de entrenamiento.
        """
        exercises = self.db.query(ExercisePerWeekDayModel, WeekDayModel.name, TrainingPlanModel.name, UserModel.name).\
            select_from(ExercisePerWeekDayModel).\
            join(TrainingPlanModel).\
            filter(TrainingPlanModel.is_visible == True).\
            join(UserModel).\
            filter(UserModel.role_id == 3).\
            join(WeekDayModel, ExercisePerWeekDayModel.week_day_id == WeekDayModel.id).\
            all()

        return self.group_exercises_by_day_and_training_plan(exercises)

    def get_admin_excercise_per_week_day(self):
        """
        Obtiene todos los ejercicios por día de la semana para usuarios administradores.

        Precondición:
        - Ninguna.

        Postcondición:
        - Devuelve un diccionario que agrupa los ejercicios por día de la semana y plan de entrenamiento.
        """
        exercises = self.db.query(ExercisePerWeekDayModel, WeekDayModel.name, TrainingPlanModel.name, UserModel.name).\
            select_from(ExercisePerWeekDayModel).\
            join(TrainingPlanModel).\
            filter(TrainingPlanModel.is_visible == True).\
            join(UserModel).\
            filter(UserModel.role_id == 4).\
            join(WeekDayModel, ExercisePerWeekDayModel.week_day_id == WeekDayModel.id).\
            all()

        return self.group_exercises_by_day_and_training_plan(exercises)

    def group_exercises_by_day_and_training_plan(self, exercises):
        """
        Agrupa los ejercicios por día de la semana y plan de entrenamiento.

        Parámetros:
        - exercises: lista de ejercicios.

        Precondición:
        - Ninguna.

        Postcondición:
        - Devuelve un diccionario que agrupa los ejercicios por día de la semana y plan de entrenamiento.
        """
        exercises_by_plan_and_day = {}
        for exercise, week_day_name, training_plan_name, user_name in exercises:
            if training_plan_name not in exercises_by_plan_and_day:
                exercises_by_plan_and_day[training_plan_name] = {
                    "created by": user_name,
                    "days": {}
                }
            if week_day_name not in exercises_by_plan_and_day[training_plan_name]["days"]:
                exercises_by_plan_and_day[training_plan_name]["days"][week_day_name] = []
            exercises_by_plan_and_day[training_plan_name]["days"][week_day_name].append(exercise)
        return exercises_by_plan_and_day

    def get_excercise_per_week_day_by_id(self, id, user: str):
        """
        Obtiene un ejercicio por día de la semana y ID de usuario específicos.

        Parámetros:
        - id: ID del ejercicio.
        - user: correo electrónico del usuario.

        Precondición:
        - El ejercicio y el usuario deben existir en la base de datos.

        Postcondición:
        - Devuelve el ejercicio y el nombre del día de la semana correspondiente.
        """
        return self.db.query(ExercisePerWeekDayModel, WeekDayModel.name).join(WeekDayModel).filter(ExercisePerWeekDayModel.id == id, TrainingPlanModel.user_email == user).first()

    def create_new_excercise_per_week_day(self, exercise_per_week_day: ExercisePerWeekDay):
        """
        Crea un nuevo ejercicio por día de la semana.

        Parámetros:
        - exercise_per_week_day: objeto ExercisePerWeekDay que contiene los datos del ejercicio.

        Precondición:
        - Ninguna.

        Postcondición:
        - Crea un nuevo ejercicio por día de la semana en la base de datos y lo devuelve.
        """
        new_excercise_per_week_day = ExercisePerWeekDayModel(**exercise_per_week_day.model_dump())

        self.db.add(new_excercise_per_week_day)
        self.db.commit()
        self.db.refresh(new_excercise_per_week_day)
        return new_excercise_per_week_day

    def delete_excercise_per_week_day(self, id, user: str):
        """
        Elimina un ejercicio por día de la semana y ID de usuario específicos.

        Parámetros:
        - id: ID del ejercicio.
        - user: correo electrónico del usuario.

        Precondición:
        - El ejercicio y el usuario deben existir en la base de datos.

        Postcondición:
        - Elimina el ejercicio por día de la semana de la base de datos y lo devuelve.
        """
        element = self.db.query(ExercisePerWeekDayModel).\
            join(TrainingPlanModel).\
            filter(ExercisePerWeekDayModel.id == id, TrainingPlanModel.user_email == user).first()
        self.db.delete(element)
        self.db.commit()
        return element