from typing import List
from src.models.star import Star as star
from src.schemas.star import Star

class StarRepository():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all_star(self) -> List[Star]:
        query = self.db.query(star)
        return query.all()
    
    def create_new_star(self, star: Star) -> Star:
        new_star = star(**star.model_dump())
        self.db.add(new_star)

        self.db.commit()
        self.db.refresh(new_star)
        return new_star
    
    def delete_star(self, id: int) -> dict:
        query = self.db.query(star).filter(star.id == id)
        star = query.first()
        self.db.delete(star)
        self.db.commit()
        return {"message": "Star deleted successfully"}
    
    def update_star(self, id: int, star: Star) -> Star:
        query = self.db.query(star).filter(star.id == id)
        star_db = query.first()
        star_db.name = star.name
        star_db.description = star.description
        self.db.commit()
        self.db.refresh(star_db)
        return star_db
    
    def get_star_by_id(self, id: int) -> Star:
        query = self.db.query(star).filter(star.id == id)
        return query.first()
    
    def get_star_by_training_plan_id(self, training_plan_id: int) -> List[Star]:
        query = self.db.query(star).filter(star.training_plan_id == training_plan_id)
        return query.all()