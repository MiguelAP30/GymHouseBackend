from typing import List
from src.models.specific_muscle import SpecificMuscle as specific_muscle
from src.schemas.specific_muscle import SpecificMuscle

class SpecificMuscleRepository():
    def __init__(self, db) -> None:
        self.db = db

    def get_all_specific_muscle(self) -> List[SpecificMuscle]:
        query = self.db.query(specific_muscle)
        return query.all()
    
    def create_new_specific_muscle(self, specific_muscle: SpecificMuscle) -> SpecificMuscle:
        new_specific_muscle = specific_muscle(**specific_muscle.model_dump())
        self.db.add(new_specific_muscle)

        self.db.commit()
        self.db.refresh(new_specific_muscle)
        return new_specific_muscle
    
    def delete_specific_muscle(self, id: int) -> dict:
        query = self.db.query(specific_muscle).filter(specific_muscle.id == id)
        result = query.first()
        self.db.delete(result)
        self.db.commit()
        return {"message": "The specific muscle was successfully deleted", "data": None}
    
    def update_specific_muscle(self, id: int, specific_muscle: SpecificMuscle) -> SpecificMuscle:
        query = self.db.query(specific_muscle).filter(specific_muscle.id == id)
        result = query.first()
        result.name = specific_muscle.name
        self.db.commit()
        self.db.refresh(result)
        return result
    
    def get_specific_muscle_by_id(self, id: int) -> SpecificMuscle:
        query = self.db.query(specific_muscle).filter(specific_muscle.id == id)
        return query.first()
    
    