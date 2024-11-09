from typing import List
from src.schemas.tag_of_training_plan import TagOfTrainingPlan
from src.models.tag_of_training_plan import TagOfTrainingPlan as tag_of_training_plans

class TagOfTrainingPlanRepository():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all_tag_of_training_plans(self) -> List[TagOfTrainingPlan]:
        query = self.db.query(tag_of_training_plans)
        return query.all()
    
    def get_tag_of_training_plan_by_id(self, id: int ):
        element = self.db.query(tag_of_training_plans).filter(tag_of_training_plans.id == id).first()
        return element
    
    def delete_tag_of_training_plan(self, id: int ) -> dict:
        element: TagOfTrainingPlan= self.db.query(tag_of_training_plans).filter(tag_of_training_plans.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element

    def create_new_tag_of_training_plan(self, tag_of_training_plan:TagOfTrainingPlan ) -> dict:
        new_tag_of_training_plan = tag_of_training_plans(**tag_of_training_plan.model_dump())
        self.db.add(new_tag_of_training_plan)
        
        self.db.commit()
        self.db.refresh(new_tag_of_training_plan)
        return new_tag_of_training_plan
    
    def update_tag_of_training_plan(self, id: int, tag_of_training_plan: TagOfTrainingPlan) -> dict:
        element = self.db.query(tag_of_training_plans).filter(tag_of_training_plans.id == id).first()
        element.name = tag_of_training_plan.name

        self.db.commit()
        self.db.refresh(element)
        return element