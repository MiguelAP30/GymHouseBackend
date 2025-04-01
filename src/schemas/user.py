from pydantic import BaseModel, EmailStr, Field, validator, model_validator
from typing import List, Optional

class User(BaseModel):
    email: EmailStr = Field(min_length=6, title="Email del usuario", max_length=250, example="hola@gmail.com")
    id_number: str = Field(min_length=6, title="Numero de identificacion del usuario", max_length=20, example="123456789")
    password: str = Field(min_length=6,title="Contraseña del usuario", max_length=255, example="123456")
    user_name: Optional[str] = Field(default=None, min_length=6, title="Nombre de usuario", max_length=50, example="hola123")
    name: str = Field(min_length=2, title="Nombre del usuario", max_length=50, example="Miguel Angel")
    phone: str = Field(min_length=8, title="Telefono del usuario", max_length=20, example="12345678")
    address: Optional[str] = Field(default=None, min_length=8, title="Direccion del usuario", max_length=150, example="Calle 123")
    birth_date: str = Field(title="Fecha de nacimiento del usuario", example="2003-11-12")
    gender: str = Field(min_length=1,title="Genero del usuario", max_length=1, example="m")
    status: Optional[bool] = Field(default= True, title="Estado del usuario", example=True)
    start_date: Optional[str] = Field(default=None, title="Fecha de inicio del usuario", example="2021-11-12")
    final_date: Optional[str] = Field(default=None, title="Fecha de finalizacion del usuario", example="2021-12-12")
    role_id: Optional[int] = Field(default= 1, title="Rol del usuario", ge=1, example=4)

class UserLogin (BaseModel):
    email: EmailStr = Field(min_length=6, max_length=64, alias="email", title="Correo del usuario")
    password: str = Field(min_length=6, title="Contraseña del usuario")

class ChangePassword(BaseModel):
    current_password: str = Field(min_length=6, title="Contraseña actual del usuario")
    new_password: str = Field(min_length=6, title="Nueva contraseña del usuario")

class ResetPassword(BaseModel):
    email: EmailStr = Field(min_length=6, max_length=64, title="Correo del usuario")
    new_password: str = Field(min_length=6, title="Nueva contraseña del usuario")
    reset_token: str = Field(title="Token de restablecimiento de contraseña")

class UpdateUser(BaseModel):
    id_number: str = Field(min_length=6, title="Numero de identificacion del usuario", max_length=20, example="123456789")
    user_name: Optional[str] = Field(default=None, min_length=6, title="Nombre de usuario", max_length=50, example="hola123")
    name: str = Field(min_length=2, title="Nombre del usuario", max_length=50, example="Miguel Angel")
    phone: str = Field(min_length=8, title="Telefono del usuario", max_length=20, example="12345678")
    address: Optional[str] = Field(default=None, min_length=8, title="Direccion del usuario", max_length=150, example="Calle 123")
    birth_date: str = Field(title="Fecha de nacimiento del usuario", example="2003-11-12")
    gender: str = Field(min_length=1,title="Genero del usuario", max_length=1, example="m")
