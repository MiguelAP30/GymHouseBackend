from typing import List
from src.models.specific_muscle import SpecificMuscle as SpecificMuscleModel
from src.schemas.specific_muscle import SpecificMuscle
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status

class SpecificMuscleRepository():
    def __init__(self, db) -> None:
        self.db = db

    def get_all_specific_muscle(self) -> List[SpecificMuscle]:
        query = self.db.query(SpecificMuscleModel)
        return query.all()
    
    def create_new_specific_muscle(self, specific_muscle: SpecificMuscle) -> SpecificMuscle:
        new_specific_muscle = SpecificMuscleModel(**specific_muscle.model_dump())
        self.db.add(new_specific_muscle)

        self.db.commit()
        self.db.refresh(new_specific_muscle)
        return new_specific_muscle
    
    def delete_specific_muscle(self, id: int) -> dict:
        element = self.db.query(SpecificMuscleModel).filter(SpecificMuscleModel.id == id).first()
        if not element:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Músculo específico no encontrado"
            )
        # Guardamos los datos antes de eliminar
        deleted_data = jsonable_encoder(element)
        self.db.delete(element)
        self.db.commit()
        return deleted_data
    
    def update_specific_muscle(self, id: int, specific_muscle: SpecificMuscle) -> dict:
        element = self.db.query(SpecificMuscleModel).filter(SpecificMuscleModel.id == id).first()
        if not element:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Músculo específico no encontrado"
            )
        element.name = specific_muscle.name
        element.muscle_id = specific_muscle.muscle_id
        element.description = specific_muscle.description
        self.db.commit()
        self.db.refresh(element)
        return jsonable_encoder(element)
    
    def get_specific_muscle_by_id(self, id: int) -> SpecificMuscle:
        element = self.db.query(SpecificMuscleModel).filter(SpecificMuscleModel.id == id).first()
        if not element:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Músculo específico no encontrado"
            )
        return element
    
    