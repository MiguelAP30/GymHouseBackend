from fastapi import APIRouter, Body, Query, Path, status
from fastapi.responses import JSONResponse
from typing import List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.schemas.week_day import WeekDay
from src.models.week_day import WeekDay as week_days
from src.repositories.week_day import WeekDayRepository

week_day_router = APIRouter(tags=['Días de la semana'])

#CRUD week_day

@week_day_router.get('',response_model=List[WeekDay],description="Devuelve todos los días de la semana")
def get_week_days()-> List[WeekDay]:
    db= SessionLocal()
    result = WeekDayRepository(db).get_all_week_days()
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)

@week_day_router.get('/{id}',response_model=WeekDay,description="Devuelve la información de un solo día de la semana")
def get_week_day(id: int = Path(ge=1)) -> WeekDay:
    db = SessionLocal()
    element=  WeekDayRepository(db).get_week_day_by_id(id)
    if not element:        
        return JSONResponse(
            content={            
                "message": "The requested week day was not found",            
                "data": None        
                }, 
            status_code=status.HTTP_404_NOT_FOUND
            )    
    return JSONResponse(
        content=jsonable_encoder(element),                        
        status_code=status.HTTP_200_OK
        )

@week_day_router.post('',response_model=dict,description="Crea un nuevo día de la semana")
def create_week_day(week_day: WeekDay = Body()) -> dict:
    db= SessionLocal()
    new_week_day = WeekDayRepository(db).create_new_week_day(week_day)
    return JSONResponse(
        content={        
        "message": "The week day was successfully created",        
        "data": jsonable_encoder(new_week_day)    
        }, 
        status_code=status.HTTP_201_CREATED
    )

@week_day_router.delete('/{id}',response_model=dict,description="Elimina un día de la semana específico")
def remove_week_day(id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    element = WeekDayRepository(db).delete_week_day(id)
    if not element:        
        return JSONResponse(
            content={            
                "message": "The requested week day was not found",            
                "data": None        
                }, 
            status_code=status.HTTP_404_NOT_FOUND
            )
    return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)

@week_day_router.put('/{id}',response_model=dict,description="Actualiza un día de la semana específico")
def update_week_day(id: int = Path(ge=1), week_day: WeekDay = Body()) -> dict:
    db = SessionLocal()
    element = WeekDayRepository(db).update_week_day(id, week_day)
    if not element:        
        return JSONResponse(
            content={            
                "message": "The requested week day was not found",            
                "data": None        
                }, 
            status_code=status.HTTP_404_NOT_FOUND
            )
    return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)