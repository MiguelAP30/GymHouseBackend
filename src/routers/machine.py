from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.schemas.machine import Machine
from src.models.machine import Machine as machines
from src.repositories.machine import MachineRepository
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler

machine_router = APIRouter(tags=['Máquinas'])

#CRUD machine

@machine_router.get('',response_model=List[Machine],description="Devuelve todas las máquinas")
def get_machines()-> List[Machine]:
    db= SessionLocal()
    result = MachineRepository(db).get_all_machines()
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)

@machine_router.get('/{id}',response_model=Machine,description="Devuelve la información de una sola máquina")
def get_machine( id: int = Path(ge=1)) -> Machine:
    db = SessionLocal()
    element=  MachineRepository(db).get_machine_by_id(id)
    if not element:        
        return JSONResponse(
            content={            
                "message": "The requested machine was not found",            
                "data": None        
                }, 
            status_code=status.HTTP_404_NOT_FOUND
            )    
    return JSONResponse(
        content=jsonable_encoder(element),                        
        status_code=status.HTTP_200_OK
        )

@machine_router.post('',response_model=dict,description="Crea una nueva máquina")
def create_machine(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], machine: Machine = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user > 3:
            if status_user:
                new_machine = MachineRepository(db).create_new_machine(machine)
                return JSONResponse(
                    content={        
                    "message": "The machine was successfully created",        
                    "data": jsonable_encoder(new_machine)    
                    }, 
                    status_code=status.HTTP_201_CREATED
                )
            else:
                return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@machine_router.delete('/{id}',response_model=dict,description="Elimina una máquina específica")
def remove_machine(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user > 3:
            if status_user:
                element = MachineRepository(db).delete_machine(id)
                if not element:        
                    return JSONResponse(
                        content={            
                            "message": "The requested machine was not found",            
                            "data": None        
                            }, 
                        status_code=status.HTTP_404_NOT_FOUND
                        )    
                return JSONResponse(
                    content={        
                    "message": "The machine was successfully deleted",        
                    "data": None    
                    }, 
                    status_code=status.HTTP_200_OK
                )
            else:
                return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@machine_router.put('/{id}',response_model=dict,description="Actualiza una máquina específica")
def update_machine(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), machine: Machine = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user > 3:
            if status_user:
                updated_machine = MachineRepository(db).update_machine(id, machine)
                if not updated_machine:
                    return JSONResponse(
                        content={            
                            "message": "The requested machine was not found",            
                            "data": None        
                            }, 
                        status_code=status.HTTP_404_NOT_FOUND
                        )    
                return JSONResponse(
                    content={        
                    "message": "The machine was successfully updated",        
                    "data": jsonable_encoder(updated_machine)    
                    }, 
                    status_code=status.HTTP_200_OK
                )
            else:
                return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@machine_router.post('/init', response_model=dict, description="Inicializa máquinas específicas en la base de datos")
def init_machine(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)]) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3:
            if status_user:
                machines_data = [
                    {"name": "Barra Olímpica", "description": "Una barra de acero utilizada en levantamientos compuestos como sentadillas, peso muerto y press de banca. Es fundamental para entrenamientos de fuerza y levantamiento olímpico."},
                    {"name": "Mancuernas", "description": "Pesos libres utilizados para entrenar de forma unilateral, lo que ayuda a equilibrar la fuerza entre ambos lados del cuerpo. Permiten una amplia variedad de ejercicios."},
                    {"name": "Máquina de Fuerza", "description": "Dispositivos mecánicos que guían el movimiento y permiten entrenar músculos específicos de manera controlada y segura, reduciendo el riesgo de lesiones."},
                    {"name": "Peso Corporal", "description": "Ejercicios que utilizan el peso del cuerpo como resistencia, como flexiones, sentadillas o dominadas, promoviendo fuerza funcional y estabilidad."},
                    {"name": "Banda Elástica", "description": "Bandas de resistencia que añaden tensión progresiva a los movimientos. Ideales para entrenar músculos estabilizadores, rehabilitación y movilidad."},
                    {"name": "Kettlebell", "description": "Pesas con forma de bola y una manija. Se utilizan para entrenamientos dinámicos que mejoran la fuerza, la potencia y la resistencia cardiovascular."},
                    {"name": "Balón Medicinal", "description": "Pelotas pesadas que se usan para mejorar la potencia explosiva, la coordinación y la estabilidad del núcleo mediante ejercicios dinámicos."},
                    {"name": "Cables", "description": "Sistema de poleas que permite movimientos multidireccionales y trabajar diferentes músculos. Ideal para entrenamientos funcionales y específicos."},
                    {"name": "Caja Plyo", "description": "Plataforma elevada utilizada para ejercicios pliométricos como saltos, que mejoran la potencia explosiva, agilidad y coordinación."},
                    {"name": "Banco", "description": "Superficie de apoyo para realizar ejercicios con mancuernas, barras u otros equipos. Es fundamental en ejercicios como press de banca y abdominales."},
                    {"name": "Máquina Smith", "description": "Barra guiada que se mueve verticalmente, ideal para entrenar con mayor estabilidad y seguridad en ejercicios de fuerza como sentadillas y press de banca."},
                    {"name": "Estiramientos", "description": "Herramientas o zonas diseñadas para realizar ejercicios de estiramiento que mejoran la flexibilidad y la movilidad, fundamentales para la recuperación."},
                    {"name": "Cardio", "description": "Máquinas como bicicletas estáticas, cintas de correr y elípticas, usadas para mejorar la resistencia cardiovascular y quemar calorías."},
                    {"name": "TRX", "description": "Sistema de suspensión que permite realizar ejercicios de peso corporal con énfasis en la estabilidad del núcleo y la fuerza funcional."},
                    {"name": "Bosu Ball", "description": "Medio balón inflable utilizado para ejercicios de equilibrio, estabilidad y fortalecimiento del núcleo. Ideal para entrenamiento funcional."},
                    {"name": "Recuperación", "description": "Máquinas y equipos utilizados para estiramientos, masajes y otros ejercicios enfocados en la recuperación muscular después del entrenamiento."},
                    {"name": "Yoga", "description": "Espacios y accesorios como colchonetas y bloques utilizados para la práctica de yoga, mejorando la flexibilidad, equilibrio y relajación."},
                    {"name": "Plato", "description": "Pesas circulares que se agregan a barras o se usan de manera independiente para aumentar la carga en levantamientos de fuerza."},
                ]
                
                created_machines = []
                for machine_data in machines_data:
                    if not db.query(machines).filter_by(name=machine_data["name"]).first():
                        new_machine = machines(**machine_data)
                        db.add(new_machine)
                        created_machines.append(new_machine)
                
                db.commit()
                return JSONResponse(
                    content={
                        "message": "Las máquinas se han inicializado correctamente",
                        "data": jsonable_encoder(created_machines)
                    },
                    status_code=status.HTTP_201_CREATED
                )
            else:
                return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)