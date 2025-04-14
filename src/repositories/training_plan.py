from typing import List
from src.schemas.training_plan import TrainingPlan
from src.models.training_plan import TrainingPlan as training_plans
from src.models.user import User
from src.models.workout_day_exercise import WorkoutDayExercise as WorkoutDayExerciseModel
from src.models.week_day import WeekDay as WeekDayModel

class TrainingPlanRepository():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all_training_plans(self, ) -> List[TrainingPlan]:
        query = self.db.query(training_plans).\
        filter(training_plans.is_visible == True)
        return query.all()
    
    def get_all_training_plans_by_role_admin(self) -> List[TrainingPlan]:
        query = self.db.query(training_plans).join(User, training_plans.user_email == User.email).filter(User.role_id == 4, training_plans.is_visible == True)
        return query.all()
    
    def get_all_training_plans_by_role_gym(self) -> List[TrainingPlan]:
        query = self.db.query(training_plans).join(User, training_plans.user_email == User.email).filter(User.role_id == 3, training_plans.is_visible == True)
        return query.all()
    
    def get_all_training_plans_by_role_premium(self) -> List[TrainingPlan]:
        query = self.db.query(training_plans).join(User, training_plans.user_email == User.email).filter(User.role_id == 2, training_plans.is_visible == True)
        return query.all()
    
    def get_all_my_training_plans(self, user_email: str) -> List[TrainingPlan]:
        query = self.db.query(training_plans).join(User, training_plans.user_email == User.email).filter(training_plans.user_email == user_email)
        return query.all()
    
    def get_training_plan_by_id(self, id: int, user: str):
        element = self.db.query(training_plans).\
        filter(training_plans.id == id, training_plans.user_email == user).first()
        return element
    
    def delete_training_plan(self, id: int, user: str) -> dict:
        element = self.db.query(training_plans).\
        filter(training_plans.id == id, training_plans.user_email == user).first()
        self.db.delete(element)
        self.db.commit()
        return element

    def create_new_training_plan(self, training_plan:TrainingPlan ) -> dict:
        # Crear el nuevo plan de entrenamiento
        new_training_plan = training_plans(**training_plan.model_dump())
        self.db.add(new_training_plan)
        self.db.commit()
        self.db.refresh(new_training_plan)

        # Obtener todos los días de la semana
        week_days = self.db.query(WeekDayModel).all()

        # Crear un workout_day_exercise para cada día de la semana
        for week_day in week_days:
            new_workout_day_exercise = WorkoutDayExerciseModel(
                week_day_id=week_day.id,
                training_plan_id=new_training_plan.id
            )
            self.db.add(new_workout_day_exercise)

        self.db.commit()
        return new_training_plan

    def update_training_plan(self, id: int, training_plan: TrainingPlan, user: str) -> dict:
        element = self.db.query(training_plans).\
        filter(training_plans.id == id, training_plans.user_email == user).first()
        element.name = training_plan.name
        element.description = training_plan.description
        element.tag_of_training_plan_id = training_plan.tag_of_training_plan_id

        self.db.commit()
        self.db.refresh(element)
        return element