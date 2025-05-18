from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List, Optional
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.schemas.training_plan import TrainingPlan, PaginatedTrainingPlanResponse, TrainingPlanCreate, TrainingPlanCreateByGym, TrainingPlanUpdate
from src.models.training_plan import TrainingPlan as training_plans
from src.repositories.training_plan import TrainingPlanRepository
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler

training_plan_router = APIRouter(tags=['Planes de entrenamiento'])

@training_plan_router.get('', response_model=PaginatedTrainingPlanResponse, description="Retorna todos los planes de entrenamiento con paginación y filtros")
def get_training_plans(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Tamaño de la página"),
    name: Optional[str] = Query(None, description="Texto para buscar en el nombre"),
    role_id: Optional[int] = Query(None, description="ID del rol del usuario para filtrar"),
    tag_id: Optional[int] = Query(None, description="ID de la etiqueta para filtrar"),
    max_days: Optional[int] = Query(None, description="Cantidad máxima de días de la semana")
) -> PaginatedTrainingPlanResponse:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user == False:
            return JSONResponse(content={"message": "Your account is disabled", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        
        # Obtener planes de entrenamiento con paginación y filtros
        training_plans_list, total = TrainingPlanRepository(db).get_all_training_plans(
            page=page,
            size=size,
            search_name=name,
            role_id=role_id,
            tag_id=tag_id,
            max_days=max_days
        )
        
        # Calcular el número total de páginas
        total_pages = (total + size - 1) // size
        
        # Convertir los objetos a diccionarios
        training_plans_dict = [jsonable_encoder(plan) for plan in training_plans_list]
        
        # Crear la respuesta paginada
        paginated_response = PaginatedTrainingPlanResponse(
            items=training_plans_dict,
            total=total,
            page=page,
            size=size,
            pages=total_pages
        )
        
        return JSONResponse(content=jsonable_encoder(paginated_response), status_code=status.HTTP_200_OK)

@training_plan_router.get('/my', response_model=List[TrainingPlan], description="Retorna todos los planes de entrenamiento creados por el usuario actual")
def get_my_training_plans(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> List[TrainingPlan]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user == False:
            return JSONResponse(content={"message": "Your account is disabled", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        
        current_user = payload.get("sub")
        result = TrainingPlanRepository(db).get_all_my_training_plans(current_user)
        return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)

@training_plan_router.get('/user/{email}', response_model=List[TrainingPlan], description="Retorna todos los planes de entrenamiento de un usuario específico")
def get_user_training_plans(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    email: str = Path(min_length=5)
) -> List[TrainingPlan]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user == False:
            return JSONResponse(content={"message": "Your account is disabled", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        result = TrainingPlanRepository(db).get_all_training_plans_by_email(email)
        return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)

@training_plan_router.get('/{id}', response_model=TrainingPlan, description="Retorna un solo plan de entrenamiento")
def get_training_plan_by_id(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1)) -> TrainingPlan:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        current_user = payload.get("sub")

        if not status_user:
            return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        
        if role_current_user < 2:
            return JSONResponse(content={"message": "Privilegios insuficientes", "data": None}, status_code=status.HTTP_403_FORBIDDEN)

        repo = TrainingPlanRepository(db)
        try:
            existing_plan = repo.get_training_plan_by_id(id)
            if not existing_plan:
                return JSONResponse(content={"message": "El plan no fue encontrado", "data": None}, status_code=status.HTTP_404_NOT_FOUND)

            # Si el plan es visible, lo puede ver cualquiera con rol >= 2 y cuenta activa
            if existing_plan.is_visible:
                response = jsonable_encoder(existing_plan)
                permissions = repo.check_user_permissions_on_training_plan(id, current_user)
                response['permissions'] = permissions
                return JSONResponse(content={"message": "Plan obtenido exitosamente", "data": response}, status_code=status.HTTP_200_OK)

            # Si no es visible, chequear permisos con la función que definiste
            permissions = repo.check_user_permissions_on_training_plan(id, current_user)
            if not (permissions["can_edit"] or role_current_user == 4):
                return JSONResponse(content={"message": "No tienes permiso para ver este plan", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
            
            response = jsonable_encoder(existing_plan)
            response['permissions'] = permissions
            return JSONResponse(content={"message": "Plan obtenido exitosamente", "data": response}, status_code=status.HTTP_200_OK)

        except Exception as e:
            return JSONResponse(content={"message": f"Error al obtener el plan: {str(e)}", "data": None}, status_code=status.HTTP_400_BAD_REQUEST)
    
@training_plan_router.post('/me', response_model=dict, description="Un usuario premium crea su propio plan")
def create_training_plan_as_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], training_plan: TrainingPlanCreate = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        user_email = payload.get("sub")
        role = payload.get("user.role")
        status_user = payload.get("user.status")

        if role < 2:
            return JSONResponse(content={"message": "Solo usuarios premium pueden crear planes propios"}, status_code=status.HTTP_403_FORBIDDEN)
        if not status_user:
            return JSONResponse(content={"message": "Tu cuenta está inactiva"}, status_code=status.HTTP_403_FORBIDDEN)

        training_plan.user_email = user_email  # Seguridad: fuerza el email
        try:
            new_plan = TrainingPlanRepository(db).create_training_plan_as_user(training_plan, user_email)
            return JSONResponse(content={"message": "Plan creado exitosamente", "data": jsonable_encoder(new_plan)}, status_code=status.HTTP_201_CREATED)
        except ValueError as e:
            return JSONResponse(content={"message": str(e), "data": None}, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JSONResponse(content={"message": "Error interno del servidor", "error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@training_plan_router.post('/gym', response_model=dict, description="Un gimnasio crea un plan para un usuario asociado")
def create_training_plan_by_gym(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], training_plan: TrainingPlanCreateByGym = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        gym_email = payload.get("sub")
        role = payload.get("user.role")
        status_user = payload.get("user.status")

        if role < 3:
            return JSONResponse(content={"message": "Solo gimnasios o administradores pueden usar esta función"}, status_code=status.HTTP_403_FORBIDDEN)
        if not status_user:
            return JSONResponse(content={"message": "Tu cuenta está inactiva"}, status_code=status.HTTP_403_FORBIDDEN)
        
        try:
            new_plan = TrainingPlanRepository(db).create_plan_for_user_from_gym(training_plan, gym_email)
            return JSONResponse(content={"message": "Plan creado por gimnasio exitosamente", "data": jsonable_encoder(new_plan)}, status_code=status.HTTP_201_CREATED)
        except ValueError as e:
            return JSONResponse(content={"message": str(e), "data": None}, status_code=status.HTTP_400_BAD_REQUEST)


@training_plan_router.delete('/{id}', response_model=dict, description="Elimina un plan de entrenamiento")
def delete_training_plan(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        user_email = payload.get("sub")
        role = payload.get("user.role")
        status_user = payload.get("user.status")

        if role < 2:
            return JSONResponse(content={"message": "No tienes permisos suficientes"}, status_code=status.HTTP_403_FORBIDDEN)
        if not status_user:
            return JSONResponse(content={"message": "Cuenta inactiva"}, status_code=status.HTTP_403_FORBIDDEN)

    try:
        deleted = TrainingPlanRepository(db).delete_training_plan(id, user_email)
        return JSONResponse(content={"message": "Plan eliminado exitosamente", "data": jsonable_encoder(deleted)}, status_code=status.HTTP_200_OK)
    except ValueError as e:
        return JSONResponse(content={"message": str(e), "data": None}, status_code=status.HTTP_400_BAD_REQUEST)

@training_plan_router.put('/{id}', response_model=dict, description="Actualiza un plan de entrenamiento")
def update_training_plan(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1), training_plan: TrainingPlanUpdate = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        user_email = payload.get("sub")
        role = payload.get("user.role")
        status_user = payload.get("user.status")

        if role < 2:
            return JSONResponse(content={"message": "No tienes permisos suficientes"}, status_code=status.HTTP_403_FORBIDDEN)
        if not status_user:
            return JSONResponse(content={"message": "Tu cuenta está inactiva"}, status_code=status.HTTP_403_FORBIDDEN)

    try:
        updated = TrainingPlanRepository(db).update_training_plan(id, training_plan, user_email)
        return JSONResponse(content={"message": "Plan actualizado correctamente", "data": jsonable_encoder(updated)}, status_code=status.HTTP_200_OK)
    except ValueError as e:
        return JSONResponse(content={"message": str(e), "data": None}, status_code=status.HTTP_400_BAD_REQUEST)
