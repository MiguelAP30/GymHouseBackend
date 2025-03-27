from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional

class Gym(BaseModel):
    id: Optional[int] = Field(default=None, title="Id del gimnasio")
    user_email: str = Field(title="Email del usuario")
    name: str = Field(title="Nombre del gimnasio")
    address: str = Field(title="Dirección del gimnasio")
    phone: str = Field(title="Teléfono del gimnasio")
    email: str = Field(title="Email del gimnasio")
    website: str = Field(title="Sitio web del gimnasio")
    open_time: str = Field(title="Hora de apertura del gimnasio")
    close_time: str = Field(title="Hora de cierre del gimnasio")
    price: float = Field(title="Precio de la membresía")
    description: str = Field(title="Descripción del gimnasio")
    image: str = Field(title="Imagen del gimnasio")
    city: str = Field(title="Ciudad del gimnasio")
    country: str = Field(title="País del gimnasio")
    start_date: str = Field(title="Fecha de inicio de la membresía")
    final_date: str = Field(title="Fecha de finalización de la membresía")
    is_active: bool = Field(title="Estado del gimnasio")
    
    @validator("price")
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("El precio debe ser positivo")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_email": "hola@gmail.com",
                "name": "Gym A",
                "address": "Av. 123",
                "phone": "123456789",
                "email": "hola@gmail.com",
                "website": "www.gyma.com",
                "open_time": "08:00",
                "close_time": "20:00",
                "price": 100.0,
                "description": "Gym A description",
                "image": "gyma.jpg",
                "city": "Lima",
                "country": "Perú",
                "start_date": "2021-11-12",
                "final_date": "2022-11-12",
                "is_active": True
            }
        }

class GymUpdate(BaseModel):
    name: str = Field(title="Nombre del gimnasio")
    address: str = Field(title="Dirección del gimnasio")
    phone: str = Field(title="Teléfono del gimnasio")
    email: str = Field(title="Email del gimnasio")
    website: str = Field(title="Sitio web del gimnasio")
    open_time: str = Field(title="Hora de apertura del gimnasio")
    close_time: str = Field(title="Hora de cierre del gimnasio")
    price: float = Field(title="Precio de la membresía")
    description: str = Field(title="Descripción del gimnasio")
    image: str = Field(title="Imagen del gimnasio")
    city: str = Field(title="Ciudad del gimnasio")
    country: str = Field(title="País del gimnasio")
    start_date: str = Field(title="Fecha de inicio de la membresía")
    final_date: str = Field(title="Fecha de finalización de la membresía")
    is_active: bool = Field(title="Estado del gimnasio")
    
    @validator("price")
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("El precio debe ser positivo")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Gym A",
                "address": "Av. 123",
                "phone": "123456789",
                "email": "hola@gmail.com",
                "website": "www.gyma.com",
                "open_time": "08:00",
                "close_time": "20:00",
                "price": 100.0,
                "description": "Gym A description",
                "image": "gyma.jpg",
                "city": "Lima",
                "country": "Perú",
                "start_date": "2021-11-12",
                "final_date": "2022-11-12",
                "is_active": True
            }
        }

class GymCreate(BaseModel):
    name: str = Field(title="Nombre del gimnasio")
    address: str = Field(title="Dirección del gimnasio")
    phone: str = Field(title="Teléfono del gimnasio")
    email: str = Field(title="Email del gimnasio")
    website: str = Field(title="Sitio web del gimnasio")
    open_time: str = Field(title="Hora de apertura del gimnasio")
    close_time: str = Field(title="Hora de cierre del gimnasio")
    price: float = Field(title="Precio de la membresía")
    description: str = Field(title="Descripción del gimnasio")
    image: str = Field(title="Imagen del gimnasio")
    city: str = Field(title="Ciudad del gimnasio")
    country: str = Field(title="País del gimnasio")
    start_date: str = Field(title="Fecha de inicio de la membresía")
    final_date: str = Field(title="Fecha de finalización de la membresía")
    is_active: bool = Field(title="Estado del gimnasio")
    
    @validator("price")
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("El precio debe ser positivo")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Gym A",
                "address": "Av. 123",
                "phone": "123456789",
                "email": "hola@gmail.com",
                "website": "www.gyma.com",
                "open_time": "08:00",
                "close_time": "20:00",
                "price": 100.0,
                "description": "Gym A description",
                "image": "gyma.jpg",
                "city": "Lima",
                "country": "Perú",
                "start_date": "2021-11-12",
                "final_date": "2022-11-12",
                "is_active": True
            }
        }
