from sqlalchemy import Column, ForeignKey, Integer, Float, Date, String, inspect, Boolean, event
from sqlalchemy.orm import relationship
from src.config.database import Base
from datetime import date

class User(Base):
    __tablename__ = "users"

    email = Column(String(length=250), primary_key=True)
    id_number = Column(String(length=20))
    password = Column(String(length=255))
    user_name = Column(String(length=50))
    name = Column(String(length=80))
    phone = Column(String(length=20))
    address = Column(String(length=150))
    birth_date = Column(Date)
    gender = Column(String(length=1))
    status = Column(Boolean, default=True)
    start_date = Column(Date)
    final_date = Column(Date)
    role_id = Column(Integer, ForeignKey("roles.id"))
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String(length=6), nullable=True)

    roles = relationship("Role", back_populates="users")
    training_plans = relationship("TrainingPlan", back_populates="users")
    likes = relationship("Like", back_populates="users")
    profiles = relationship("Profile", back_populates="users")
    history_pr_exercises = relationship("HistoryPrExercise", back_populates="users")
    gyms = relationship("Gym", back_populates="users")
    users_gyms = relationship("UserGym", back_populates="users")
    comments = relationship("Comment", back_populates="users")
    notification_tokens = relationship("NotificationToken", back_populates="user")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

@event.listens_for(User, 'load')
def check_final_date(target, context):
    """
    Evento que se dispara cuando se carga un usuario.
    Verifica si la fecha final ha pasado o no está definida y actualiza el rol si es necesario.
    Solo se aplica a usuarios que no son administradores (rol 4).
    """
    if target.role_id != 4 and (target.final_date is None or target.final_date < date.today()):
        target.role_id = 1  # Cambiar el rol a 1 (rol básico)
        # Asegurarse de que los cambios se guarden
        if context.session:
            context.session.add(target)
            context.session.commit()