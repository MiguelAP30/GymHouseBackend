from typing import List
from src.models.comment import Comment as comments
from src.schemas.comment import Comment

class CommentRepository():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all_comments(self) -> List[Comment]:
        query = self.db.query(comments)
        return query.all()
    
    def get_comment_by_id(self, id: int ):
        element = self.db.query(comments).filter(comments.id == id).first()
        return element
    
    def delete_comment(self, id: int ) -> dict:
        element: Comment= self.db.query(comments).filter(comments.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element

    def create_new_comment(self, comment:Comment ) -> dict:
        new_comment = comments(**comment.model_dump())
        self.db.add(new_comment)

        self.db.commit()
        self.db.refresh(new_comment)
        return new_comment
    
    def update_comment(self, id:int, comment:Comment) -> dict:
        element = self.db.query(comments).filter(comments.id == id).first()
        element.text = comment.text
        self.db.commit()
        self.db.refresh(element)
        return element
    
    def get_comment_by_user(self, id: int) -> List[Comment]:
        query = self.db.query(comments).filter(comments.user_id == id)
        return query.all()
    
    def get_comment_by_training_plan(self, id: int) -> List[Comment]:
        query = self.db.query(comments).filter(comments.training_plan_id == id)
        return query.all()
    

