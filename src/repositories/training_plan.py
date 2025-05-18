from typing import List, Tuple, Optional
from sqlalchemy import or_, func, and_
from src.schemas.training_plan import TrainingPlan, TrainingPlanCreate, TrainingPlanCreateByGym, TrainingPlanUpdate
from src.models.training_plan import TrainingPlan as training_plans
from src.models.user import User
from src.models.workout_day_exercise import WorkoutDayExercise as WorkoutDayExerciseModel
from src.models.week_day import WeekDay as WeekDayModel
from src.models.like import Like as LikeModel
from src.models.user_gym import UserGym
from src.repositories.user_gym import UserGymRepository
from src.models.gym import Gym
from src.repositories.gym import GymRepository


class TrainingPlanRepository():
    def __init__(self, db) -> None:
        self.db = db
        self.user_gym_repo = UserGymRepository(db)
        self.gym_repo = GymRepository(db)
    
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
    
    def delete_training_plan(self, id: int, current_user_email: str) -> dict:
        """
        Elimina un plan de entrenamiento.
        
        Args:
            id: ID del plan a eliminar
            current_user_email: Email del usuario que intenta eliminar el plan
            
        Returns:
            El plan de entrenamiento eliminado
        """
        # Obtener el plan de entrenamiento
        plan = self.db.query(training_plans).filter(training_plans.id == id).first()
        if not plan:
            raise ValueError("Plan de entrenamiento no encontrado")
            
        # Obtener el usuario actual
        current_user = self.db.query(User).filter(User.email == current_user_email).first()
        if not current_user:
            raise ValueError("Usuario no encontrado")
        # Verificar permisos
        can_delete = False

        # Si el usuario actual es administrador (role 4)
        if current_user.role_id == 4:
            can_delete = True
        # Si el usuario actual es el dueño del plan y es premium (role 2)
        elif current_user_email == plan.user_email and current_user.role_id >= 2:
            can_delete = True
        # Si el usuario actual es un gimnasio (role 3), el plan fue creado por un gym y ese gimnasio es el creador
        gym = self.gym_repo.get_gym_by_email(current_user_email)
        if current_user.role_id == 3 and plan.is_gym_created and gym:
            user_gym = self.user_gym_repo.get_user_gym(plan.user_email, gym.id)
            if user_gym and user_gym.is_active and plan.user_gym_id == user_gym.id:
                can_delete = True

        if not can_delete:
            raise ValueError("No tienes permiso para eliminar este plan de entrenamiento")
            
        self.db.delete(plan)
        self.db.commit()
        return plan


    def create_training_plan_as_user(self, training_plan: TrainingPlanCreate, current_user_email: str) -> training_plans:
        """
        Crea un nuevo plan de entrenamiento para el usuario actual.
        
        Args:
            training_plan: Datos del plan a crear
            current_user_email: Email del usuario que intenta crear el plan
            
        Returns:
            El plan de entrenamiento creado
        """
        # Obtener el usuario actual
        current_user = self.db.query(User).filter(User.email == current_user_email).first()
        if not current_user or current_user.role_id < 2:
            raise ValueError("Usuario no autorizado")

        # Verificar que el usuario actual solo cree planes para sí mismo
        if training_plan.user_email != current_user_email:
            raise ValueError("Solo puedes crear planes para ti mismo")

        # Crear el nuevo plan de entrenamiento
        new_training_plan = training_plans(
            name=training_plan.name,
            description=training_plan.description,
            tag_of_training_plan_id=training_plan.tag_of_training_plan_id,
            user_email=current_user_email,
            is_visible=training_plan.is_visible,
            is_gym_created=False
        )
        
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
    
    def create_plan_for_user_from_gym(self, training_plan: TrainingPlanCreateByGym, gym_email: str) -> training_plans:
        # Verificar que el gimnasio exista
        gym_user = self.db.query(User).filter(User.email == gym_email, User.role_id == 3).first()
        if not gym_user:
            raise ValueError("El usuario actual no es un gimnasio válido")

        # Verificar que el usuario destino exista
        target_user = self.db.query(User).filter(User.email == training_plan.user_email).first()
        if not target_user:
            raise ValueError("Usuario objetivo no encontrado")
        
        # Obtener el gimnasio desde la tabla gyms
        gym = self.gym_repo.get_gym_by_email(gym_email)
        if not gym:
            raise ValueError("No se encontró el gimnasio correspondiente al email")

        # Verificar relación activa entre gimnasio y usuario
        user_gym = self.user_gym_repo.get_user_gym(user_email=training_plan.user_email, gym_id=gym.id)
        if not user_gym or not user_gym.is_active:
            raise ValueError("El usuario no está asociado activamente al gimnasio")

        # Crear el plan
        new_plan = training_plans(
            name=training_plan.name,
            description=training_plan.description,
            tag_of_training_plan_id=training_plan.tag_of_training_plan_id,
            user_email=training_plan.user_email,
            user_gym_id=user_gym.id,
            is_visible=training_plan.is_visible,
            is_gym_created=True
        )
        self.db.add(new_plan)
        self.db.commit()
        self.db.refresh(new_plan)

        # Crear workout_day_exercise para todos los días
        week_days = self.db.query(WeekDayModel).all()
        for week_day in week_days:
            new_wde = WorkoutDayExerciseModel(
                week_day_id=week_day.id,
                training_plan_id=new_plan.id
            )
            self.db.add(new_wde)

        self.db.commit()
        return new_plan


    def update_training_plan(self, id: int, training_plan: TrainingPlanUpdate, current_user_email: str) -> dict:
        """
        Actualiza un plan de entrenamiento.
        
        Args:
            id: ID del plan a actualizar
            training_plan: Datos actualizados del plan
            current_user_email: Email del usuario que intenta actualizar el plan
            
        Returns:
            El plan de entrenamiento actualizado
        """
        # Obtener el plan de entrenamiento
        plan = self.db.query(training_plans).filter(training_plans.id == id).first()
        if not plan:
            raise ValueError("Plan de entrenamiento no encontrado")
            
        # Obtener el usuario actual
        current_user = self.db.query(User).filter(User.email == current_user_email).first()
        if not current_user:
            raise ValueError("Usuario no encontrado")
            
        # Verificar permisos
        can_update = False
        
        # Si el usuario actual es administrador (role 4)
        if current_user.role_id == 4:
            can_update = True
        # Si el usuario actual es el dueño del plan y es premium (role 2)
        elif current_user_email == plan.user_email and current_user.role_id >= 2:
            can_update = True
        # Si el usuario actual es un gimnasio (role 3), el plan fue creado por un gym y ese gimnasio es el creador
        gym = self.gym_repo.get_gym_by_email(current_user_email)
        if current_user.role_id == 3 and plan.is_gym_created and gym:
            user_gym = self.user_gym_repo.get_user_gym(plan.user_email, gym.id)
            if user_gym and user_gym.is_active and plan.user_gym_id == user_gym.id:
                can_update = True
        
        if not can_update:
            raise ValueError("No tienes permiso para actualizar este plan de entrenamiento")
            
        # Actualizar los datos del plan
        for key, value in training_plan.model_dump().items():
            if key != 'id' and hasattr(plan, key):
                setattr(plan, key, value)
                
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def check_user_permissions_on_training_plan(self, training_plan_id: int, user_email: str) -> dict:
        """
        Retorna un dict con flags 'can_edit' y 'can_delete' para el usuario y el training_plan.
        """
        # Obtener el plan de entrenamiento
        plan = self.db.query(training_plans).filter(training_plans.id == training_plan_id).first()
        if not plan:
            raise ValueError("Plan de entrenamiento no encontrado")
        
        # Obtener el usuario actual
        current_user = self.db.query(User).filter(User.email == user_email).first()
        if not current_user:
            raise ValueError("Usuario no encontrado")
        
        can_edit = False
        can_delete = False
        
        # Administrador (role 4)
        if current_user.role_id == 4:
            can_edit = True
            can_delete = True
        # Dueño del plan y premium (role >= 2)
        elif user_email == plan.user_email and current_user.role_id >= 2:
            can_edit = True
            can_delete = True
        # Gimnasio (role 3), plan creado por gimnasio y es el creador
        else:
            gym = self.gym_repo.get_gym_by_email(user_email)
            if gym and current_user.role_id == 3 and plan.is_gym_created:
                user_gym = self.user_gym_repo.get_user_gym(plan.user_email, gym.id)
                if user_gym and user_gym.is_active and plan.user_gym_id == user_gym.id:
                    can_edit = True
                    can_delete = True
        
        return {"can_edit": can_edit, "can_delete": can_delete}
