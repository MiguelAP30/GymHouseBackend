from typing import List
from src.models.dificulty import Dificulty as dificulty
from src.schemas.dificulty import Dificulty

class DificultyRepository():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all_dificulty(self) -> List[Dificulty]:
        query = self.db.query(dificulty)
        return query.all()

    def create_new_dificulty(self, dificulty: Dificulty) -> Dificulty:
        new_dificulty = dificulty(**dificulty.model_dump())
        self.db.add(new_dificulty)

        self.db.commit()
        self.db.refresh(new_dificulty)
        return new_dificulty
    
    def delete_dificulty(self, id: int) -> dict:
        element = self.db.query(dificulty).filter(dificulty.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element
    
    def update_dificulty(self, id: int, dificulty: Dificulty) -> Dificulty:
        element = self.db.query(dificulty).filter(dificulty.id == id).first()
        element.name = dificulty.name
        element.description = dificulty.description
        self.db.commit()
        return element
    
    def get_dificulty_by_id(self, id: int) -> Dificulty:
        element = self.db.query(dificulty).filter(dificulty.id == id).first()
        return element