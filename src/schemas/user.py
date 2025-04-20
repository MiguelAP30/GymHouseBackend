from pydantic import BaseModel, EmailStr, Field, validator, model_validator
from typing import List, Optional
from datetime import date

class UserRegister(BaseModel):
    email: EmailStr = Field(min_length=6, title="Email del usuario", max_length=250, example="hola@gmail.com")
    id_number: str = Field(min_length=6, title="Numero de identificacion del usuario", max_length=20, example="123456789")
    password: str = Field(min_length=6,title="Contraseña del usuario", max_length=255, example="123456")
    user_name: str = Field(min_length=6, title="Nombre de usuario", max_length=50, example="hola123")
    name: str = Field(min_length=2, title="Nombre del usuario", max_length=50, example="Miguel Angel")
    phone: str = Field(min_length=8, title="Telefono del usuario", max_length=20, example="12345678")
    address: str = Field(min_length=8, title="Direccion del usuario", max_length=150, example="Calle 123")
    birth_date: date = Field(title="Fecha de nacimiento del usuario", example="2003-11-12")
    gender: str = Field(min_length=1,title="Genero del usuario", max_length=1, example="m")
    message: Optional[str] = Field(default=None, title="Mensaje personalizado", example=None)

class User(BaseModel):
    email: EmailStr = Field(min_length=6, title="Email del usuario", max_length=250, example="hola@gmail.com")
    id_number: str = Field(min_length=6, title="Numero de identificacion del usuario", max_length=20, example="123456789")
    password: str = Field(min_length=6,title="Contraseña del usuario", max_length=255, example="123456")
    user_name: Optional[str] = Field(default=None, min_length=6, title="Nombre de usuario", max_length=50, example="hola123")
    name: str = Field(min_length=2, title="Nombre del usuario", max_length=50, example="Miguel Angel")
    phone: str = Field(min_length=8, title="Telefono del usuario", max_length=20, example="12345678")
    address: Optional[str] = Field(default=None, min_length=8, title="Direccion del usuario", max_length=150, example="Calle 123")
    birth_date: date = Field(title="Fecha de nacimiento del usuario", example="2003-11-12")
    gender: str = Field(min_length=1,title="Genero del usuario", max_length=1, example="m")
    status: Optional[bool] = Field(default= True, title="Estado del usuario", example=True)
    start_date: Optional[date] = Field(default=None, title="Fecha de inicio del usuario", example="2021-11-12")
    final_date: Optional[date] = Field(default=None, title="Fecha de finalizacion del usuario", example="2021-12-12")
    role_id: Optional[int] = Field(default= 1, title="Rol del usuario", ge=1, example=4)
    is_verified: Optional[bool] = Field(default=False, title="Estado de verificación del usuario", example=False)
    verification_code: Optional[str] = Field(default=None, title="Código de verificación", example=None)
    message: Optional[str] = Field(default=None, title="Mensaje personalizado", example=None)

class UserLogin (BaseModel):
    email: EmailStr = Field(min_length=6, max_length=64, alias="email", title="Correo del usuario")
    password: str = Field(min_length=6, title="Contraseña del usuario")

class ChangePassword(BaseModel):
    current_password: str = Field(min_length=6, title="Contraseña actual del usuario")
    new_password: str = Field(min_length=6, title="Nueva contraseña del usuario")

class ResetPassword(BaseModel):
    email: EmailStr = Field(min_length=6, max_length=64, title="Correo del usuario")
    new_password: str = Field(min_length=6, title="Nueva contraseña del usuario")
    reset_code: str = Field(title="Código de restablecimiento de contraseña")

class UpdateUser(BaseModel):
    id_number: str = Field(min_length=6, title="Numero de identificacion del usuario", max_length=20, example="123456789")
    user_name: Optional[str] = Field(default=None, min_length=6, title="Nombre de usuario", max_length=50, example="hola123")
    name: str = Field(min_length=2, title="Nombre del usuario", max_length=50, example="Miguel Angel")
    phone: str = Field(min_length=8, title="Telefono del usuario", max_length=20, example="12345678")
    address: Optional[str] = Field(default=None, min_length=8, title="Direccion del usuario", max_length=150, example="Calle 123")
    birth_date: date = Field(title="Fecha de nacimiento del usuario", example="2003-11-12")
    gender: str = Field(min_length=1,title="Genero del usuario", max_length=1, example="m")

class SubscriptionConfirmation(BaseModel):
    email: EmailStr = Field(title="Email del usuario")
    role_id: int = Field(title="Nuevo rol del usuario", ge=1, le=4)
    final_date: date = Field(title="Fecha de finalización de la suscripción")
    payment_id: str = Field(title="ID de la transacción de pago")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@ejemplo.com",
                "role_id": 2,
                "final_date": "2024-12-31",
                "payment_id": "tx_123456789"
            }
        }

class EnableAccount(BaseModel):
    email: EmailStr = Field(min_length=6, max_length=64, title="Correo del usuario")
    password: str = Field(min_length=6, title="Contraseña del usuario")
