from typing import List
from src.models.profile import Profile as profiles
from src.schemas.profile import Profile

class ProfileRepository():
    def __init__(self, db) -> None:
        self.db = db

    def get_all_profile(self) -> List[Profile]:
        elements = self.db.query(profiles)
        return elements.all()
    
    def create_new_profile(self, profile: Profile) -> Profile:
        new_profile = profiles(**profile.model_dump())
        self.db.add(new_profile)

        self.db.commit()
        self.db.refresh(new_profile)
        return new_profile
    
    def delete_profile(self, id: int) -> dict:
        element: Profile= self.db.query(profiles).filter(profiles.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element 

    
    def update_profile(self, id: int, profile: Profile) -> Profile:
        element = self.db.query(profiles).filter(profiles.id == id).first()
        element.name = profile.name
        element.description = profile.description
        self.db.commit()
        self.db.refresh(element)
        return element
    
    def get_profile_by_email(self, email: str) -> Profile:
        return self.db.query(profiles).filter(profiles.user_email == email).all()