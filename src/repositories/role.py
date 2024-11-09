from typing import List
from src.schemas.role import Role
from src.models.role import Role as roles

class RoleRepository():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all_roles(self) -> List[Role]:
        query = self.db.query(roles)
        return query.all()
    
    def get_role_by_id(self, id: int ):
        element = self.db.query(roles).filter(roles.id == id).first()
        return element
    
    def delete_role(self, id: int ) -> dict:
        element: Role= self.db.query(roles).filter(roles.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element

    def create_new_role(self, role:Role ) -> dict:
        new_role = roles(**role.model_dump())
        self.db.add(new_role)
        self.db.commit()
        self.db.refresh(new_role)
        return new_role
    
    def update_role(self, id: int, role: Role) -> dict:
        element = self.db.query(roles).filter(roles.id == id).first()
        element.name = role.name
        element.description = role.description
        self.db.commit()
        self.db.refresh(element)
        return element