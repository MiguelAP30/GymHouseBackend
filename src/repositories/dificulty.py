from typing import List
from src.models.dificulty import Dificulty as DificultyModel
from src.schemas.dificulty import Dificulty
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status

class DificultyRepository():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all_dificulty(self) -> List[Dificulty]:
        query = self.db.query(DificultyModel)
        return query.all()

    def create_new_dificulty(self, dificulty: Dificulty) -> Dificulty:
        new_dificulty = DificultyModel(**dificulty.model_dump())
        self.db.add(new_dificulty)

        self.db.commit()
        self.db.refresh(new_dificulty)
        return new_dificulty
    
    def delete_dificulty(self, id: int) -> dict:
        element = self.db.query(DificultyModel).filter(DificultyModel.id == id).first()
        if not element:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dificultad no encontrada"
            )
        # Guardamos los datos antes de eliminar
        deleted_data = jsonable_encoder(element)
        self.db.delete(element)
        self.db.commit()
        return deleted_data
    
    def update_dificulty(self, id: int, dificulty: Dificulty) -> dict:
        element = self.db.query(DificultyModel).filter(DificultyModel.id == id).first()
        if not element:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dificultad no encontrada"
            )
        element.name = dificulty.name
        self.db.commit()
        self.db.refresh(element)
        return jsonable_encoder(element)
    
    def get_dificulty_by_id(self, id: int) -> Dificulty:
        element = self.db.query(DificultyModel).filter(DificultyModel.id == id).first()
        if not element:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dificultad no encontrada"
            )
        return element