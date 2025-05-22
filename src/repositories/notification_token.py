from sqlalchemy.orm import Session
from src.models.notification_token import NotificationToken
from src.schemas.notification import NotificationTokenCreate

class NotificationTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_token(self, token: NotificationTokenCreate, user_email: str):
        # Primero intentamos obtener el token existente
        existing_token = self.get_token_by_token(token.token)
        
        if existing_token:
            # Si el token existe, actualizamos el usuario y el estado
            existing_token.user_email = user_email
            existing_token.is_active = token.is_active
            self.db.commit()
            self.db.refresh(existing_token)
            return existing_token
        
        # Si no existe, creamos uno nuevo
        db_token = NotificationToken(**token.dict(), user_email=user_email)
        self.db.add(db_token)
        self.db.commit()
        self.db.refresh(db_token)
        return db_token

    def get_token_by_user(self, user_email: str):
        return self.db.query(NotificationToken).filter(NotificationToken.user_email == user_email).first()

    def get_token_by_token(self, token: str):
        return self.db.query(NotificationToken).filter(NotificationToken.token == token).first()

    def update_token(self, token: str, is_active: bool):
        db_token = self.get_token_by_token(token)
        if db_token:
            db_token.is_active = is_active
            self.db.commit()
            self.db.refresh(db_token)
        return db_token

    def delete_token(self, token: str):
        db_token = self.get_token_by_token(token)
        if db_token:
            self.db.delete(db_token)
            self.db.commit()
            return True
        return False 
    
    def get_all_tokens(self):
        return self.db.query(NotificationToken).all()

    def delete_all_tokens(self):
        try:
            self.db.query(NotificationToken).delete()
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False
