from typing import List, Tuple, Optional
from sqlalchemy import or_, func
from src.schemas.training_plan import TrainingPlan
from src.models.training_plan import TrainingPlan as training_plans
from src.models.user import User
from src.models.workout_day_exercise import WorkoutDayExercise as WorkoutDayExerciseModel
from src.models.week_day import WeekDay as WeekDayModel
from src.models.like import Like as LikeModel

class TrainingPlanRepository():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all_training_plans(
        self, 
        page: int = 1, 
        size: int = 10,
        search_name: Optional[str] = None,
        role_id: Optional[int] = None,
        tag_id: Optional[int] = None,
        max_days: Optional[int] = None
    ) -> Tuple[List[TrainingPlan], int]:
        """
        Obtiene todos los planes de entrenamiento con paginación y filtros.
        
        Args:
            page: Número de página (comienza en 1)
            size: Tamaño de la página
            search_name: Texto para buscar en el nombre
            role_id: ID del rol del usuario para filtrar
            tag_id: ID de la etiqueta para filtrar
            max_days: Cantidad máxima de días de la semana
            
        Returns:
            Tuple con la lista de planes de entrenamiento y el total de registros
        """
        # Subconsulta para contar los likes por plan de entrenamiento
        likes_count = self.db.query(
            LikeModel.training_plan_id,
            func.count(LikeModel.id).label('likes_count')
        ).\
        filter(LikeModel.is_like == True).\
        group_by(LikeModel.training_plan_id).\
        subquery()
        
        # Consulta base con join a la tabla de usuarios y likes
        query = self.db.query(training_plans).\
            join(User, training_plans.user_email == User.email).\
            outerjoin(likes_count, training_plans.id == likes_count.c.training_plan_id).\
            filter(training_plans.is_visible == True)
        
        # Aplicar filtros
        if search_name:
            query = query.filter(training_plans.name.ilike(f"%{search_name}%"))
        if role_id:
            query = query.filter(User.role_id == role_id)
        if tag_id:
            query = query.filter(training_plans.tag_of_training_plan_id == tag_id)
            
        # Si se especifica max_days, necesitamos contar los días de la semana
        if max_days is not None:
            # Subconsulta para contar los días de la semana por plan
            days_count = self.db.query(
                WorkoutDayExerciseModel.training_plan_id,
                func.count(WorkoutDayExerciseModel.id).label('days_count')
            ).\
            group_by(WorkoutDayExerciseModel.training_plan_id).\
            having(func.count(WorkoutDayExerciseModel.id) <= max_days).\
            subquery()
            
            # Filtrar por los planes que tienen como máximo max_days días
            query = query.join(days_count, training_plans.id == days_count.c.training_plan_id)
            
        # Ordenar por cantidad de likes en orden descendente
        query = query.order_by(func.coalesce(likes_count.c.likes_count, 0).desc())
            
        # Contar el total de registros
        total = query.count()
        
        # Aplicar paginación
        offset = (page - 1) * size
        training_plans_list = query.offset(offset).limit(size).all()
        
        return training_plans_list, total
    
    def get_all_training_plans_by_email(self, email: str) -> List[TrainingPlan]:
        """
        Obtiene todos los planes de entrenamiento de un usuario específico por su email.
        
        Args:
            email: Email del usuario
            
        Returns:
            Lista de planes de entrenamiento del usuario
        """
        # Subconsulta para contar los likes por plan de entrenamiento
        likes_count = self.db.query(
            LikeModel.training_plan_id,
            func.count(LikeModel.id).label('likes_count')
        ).\
        filter(LikeModel.is_like == True).\
        group_by(LikeModel.training_plan_id).\
        subquery()
        
        # Consulta base con join a la tabla de usuarios y likes
        query = self.db.query(training_plans).\
            join(User, training_plans.user_email == User.email).\
            outerjoin(likes_count, training_plans.id == likes_count.c.training_plan_id).\
            filter(training_plans.user_email == email)
        
        # Ordenar por cantidad de likes en orden descendente
        query = query.order_by(func.coalesce(likes_count.c.likes_count, 0).desc())
        
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
    
    def get_training_plan_by_id(self, id: int, user: str = None):
        """
        Obtiene un plan de entrenamiento por su ID.
        
        Args:
            id: ID del plan de entrenamiento
            user: Email del usuario que solicita el plan (opcional)
            
        Returns:
            El plan de entrenamiento si existe y el usuario tiene acceso
        """
        # Consulta base para obtener el plan
        query = self.db.query(training_plans).filter(training_plans.id == id)
        
        # Si se proporciona un usuario, verificar si es el dueño
        if user:
            # Si el usuario es el dueño, permitir acceso independientemente de la visibilidad
            query = query.filter(training_plans.user_email == user)
        
        # Obtener el plan
        element = query.first()
        return element
    
    def delete_training_plan(self, id: int, user: str) -> dict:
        """
        Elimina un plan de entrenamiento por su ID.
        
        Args:
            id: ID del plan de entrenamiento
            user: Email del usuario que solicita la eliminación
            
        Returns:
            El plan de entrenamiento eliminado
        """
        element = self.db.query(training_plans).\
        filter(training_plans.id == id, training_plans.user_email == user).first()
        if element:
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
        """
        Actualiza un plan de entrenamiento por su ID.
        
        Args:
            id: ID del plan de entrenamiento
            training_plan: Datos actualizados del plan
            user: Email del usuario que solicita la actualización
            
        Returns:
            El plan de entrenamiento actualizado
        """
        element = self.db.query(training_plans).\
        filter(training_plans.id == id, training_plans.user_email == user).first()
        if element:
            element.name = training_plan.name
            element.description = training_plan.description
            element.tag_of_training_plan_id = training_plan.tag_of_training_plan_id
            element.is_visible = training_plan.is_visible

            self.db.commit()
            self.db.refresh(element)
        return element