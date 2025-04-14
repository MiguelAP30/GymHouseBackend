"""
Aplicación principal de GymHouseBackend.
"""
from fastapi import FastAPI, Body, Path
from src.middlewares.error_handler import ErrorHandler
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.routers.workout_day_exercise import workout_day_exercise_router
from src.routers.exercise import exercise_router
from src.routers.machine import machine_router
from src.routers.muscle import muscle_router
from src.routers.role import role_router
from src.routers.tag_of_training_plan import tag_of_training_plan_router
from src.routers.exercise_configuration import exercise_configuration_router
from src.routers.training_plan import training_plan_router
from src.routers.user import user_router
from src.routers.week_day import week_day_router
from src.routers.auth import auth_router
from src.routers.user_gym import user_gym_router
from src.routers.star import star_router
from src.routers.specific_muscle import specific_muscle_router
from src.routers.profile import profile_router
from src.routers.history_pr_exercise import history_pr_exercise_router
from src.routers.series_pr_exercise import series_pr_exercise_router
from src.routers.dropset_pr_exercise import dropset_pr_exercise_router
from src.routers.gym import gym_router
from src.routers.exercise_muscle import exercise_muscle_router
from src.routers.dificulty import dificulty_router
from src.routers.comment import comment_router
from src.routers.notification import notification_router

from src.config.database import Base, engine, SessionLocal
from src.config.database_init import init_data

import sys

# Crear las tablas en la base de datos solo si no estamos en modo de prueba
if "pytest" not in sys.modules:
    Base.metadata.create_all(bind=engine)

# Inicializar datos en la base de datos
def startup_event():
    db: Session = SessionLocal()
    try:
        init_data(db)
    finally:
        db.close()

##################################################
#                     Tags                       #

API_VERSION = 1

tags_metadata = []


#################################################

app = FastAPI(openapi_tags=tags_metadata, root_path=f"/api/v{API_VERSION}")


# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir el origen de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todas las cabeceras
)
#################################################
#                 Middlewares                   #

#app.add_middleware(ErrorHandler)

# origins = [
#     "http://localhost",
#     "http://localhost:8000",
#     "http://localhost:3000",
#     "http://localhost:8080",
#     "http://localhost:4000",
#     # Agrega aquí otros orígenes permitidos
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,  # Permitir estos orígenes
#     allow_credentials=True,
#     allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
#     allow_headers=["*"],  # Permitir todos los encabezados
# )

# Agregar el evento de inicio
app.add_event_handler("startup", startup_event)

#################################################
#      Router's definition (endpoints sets)     #

app.include_router(router=auth_router)
app.include_router(prefix="/user", router= user_router)
app.include_router(prefix="/role", router= role_router)
app.include_router(prefix="/week_day", router= week_day_router)
app.include_router(prefix="/muscle", router= muscle_router)
app.include_router(prefix="/specific_muscle", router= specific_muscle_router)
app.include_router(prefix="/dificulty", router= dificulty_router)
app.include_router(prefix="/machine", router= machine_router)
app.include_router(prefix="/exercise", router= exercise_router)
app.include_router(prefix="/exercise_muscle", router= exercise_muscle_router)
app.include_router(prefix="/tag_of_training_plan", router= tag_of_training_plan_router)
app.include_router(prefix="/training_plan", router= training_plan_router)
app.include_router(prefix="/exercise_configuration", router= exercise_configuration_router)
app.include_router(prefix="/workout_day_exercise", router= workout_day_exercise_router)
app.include_router(prefix="/user_gym", router= user_gym_router)
app.include_router(prefix="/star", router= star_router)
app.include_router(prefix="/profile", router= profile_router)
app.include_router(prefix="/history_pr_exercise", router= history_pr_exercise_router)
app.include_router(prefix="/series_pr_exercise", router= series_pr_exercise_router)
app.include_router(prefix="/dropset_pr_exercise", router= dropset_pr_exercise_router)
app.include_router(prefix="/gym", router= gym_router)
app.include_router(prefix="/comment", router= comment_router)
app.include_router(prefix="/notification", router= notification_router)

#################################################
