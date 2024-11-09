from typing import List
from src.schemas.week_day import WeekDay
from src.models.week_day import WeekDay as week_days

class WeekDayRepository():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all_week_days(self) -> List[WeekDay]:
        query = self.db.query(week_days)
        return query.all()
    
    def get_week_day_by_id(self, id: int ):
        element = self.db.query(week_days).filter(week_days.id == id).first()
        return element
    
    def delete_week_day(self, id: int ) -> dict:
        element: WeekDay= self.db.query(week_days).filter(week_days.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element

    def create_new_week_day(self, week_day:WeekDay ) -> dict:
        new_week_day = week_days(**week_day.model_dump())
        self.db.add(new_week_day)
        
        self.db.commit()
        self.db.refresh(new_week_day)
        return new_week_day
    
    def update_week_day(self, id: int, week_day: WeekDay) -> dict:
        element = self.db.query(week_days).filter(week_days.id == id).first()
        element.name = week_day.name

        self.db.commit()
        self.db.refresh(element)
        return element
    
    def get_week_day_by_name(self, name: str):
        element = self.db.query(week_days).filter(week_days.name == name).first()
        return element