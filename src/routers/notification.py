from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials
from src.config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from src.auth.has_access import security
from src.auth import auth_handler

from src.schemas.notification import Notification, NotificationTokenCreate
from src.repositories.notification_token import NotificationTokenRepository
from src.services.notification_service import NotificationService

notification_router = APIRouter(tags=['Notificaciones'])
notification_service = NotificationService()

@notification_router.post('/token', response_model=dict, description="Registra un token de notificación para un usuario")
def register_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], token: NotificationTokenCreate = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        user_email = payload.get("sub")
        if user_email:
            result = NotificationTokenRepository(db).create_token(token, user_email)
            return JSONResponse(
                content={
                    "message": "Token registrado exitosamente",
                    "data": jsonable_encoder(result)
                },
                status_code=status.HTTP_201_CREATED
            )
    return JSONResponse(
        content={"message": "Error al registrar el token"},
        status_code=status.HTTP_400_BAD_REQUEST
    )

@notification_router.post('/send', response_model=dict, description="Envía una notificación a un dispositivo específico")
async def send_notification(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], notification: Notification = Body()) -> dict:
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        result = await notification_service.send_notification(notification)
        if "error" in result:
            return JSONResponse(
                content={"message": "Error al enviar la notificación", "error": result["error"]},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return JSONResponse(
            content={"message": "Notificación enviada exitosamente", "data": result},
            status_code=status.HTTP_200_OK
        )
    return JSONResponse(
        content={"message": "No autorizado"},
        status_code=status.HTTP_401_UNAUTHORIZED
    ) 