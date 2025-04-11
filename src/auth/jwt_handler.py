"""
Manejador de tokens JWT.
"""
import jwt
from datetime import datetime, timedelta
import bcrypt
from fastapi import HTTPException, status
from src.repositories.user import UserRepository
from sqlalchemy.orm import Session

class JWTHandler:
    """Clase para manejar la generación y validación de tokens JWT."""
    
    def __init__(self, secret: str, algorithm: str, db: Session = None):
        """Inicializar el manejador JWT."""
        self.secret = secret
        self.algorithm = algorithm
        self.db = db
    
    def hash_password(self, password: str) -> str:
        """Hashear una contraseña."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verificar una contraseña."""
        return bcrypt.checkpw(password.encode(), hashed.encode())
    
    def encode_token(self, user) -> str:
        """Generar un token de acceso."""
        payload = {
            "exp": datetime.utcnow() + timedelta(hours=1),  # Token válido por 1 hora
            "iat": datetime.utcnow(),
            "scope": "access_token",
            "sub": user.email,
            "user.name": user.name,
            "user.id_number": user.id_number,
            "user.role": user.role_id,
            "user.status": user.status,
            "user.is_verified": user.is_verified,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)
    
    def decode_token(self, token: str) -> dict:
        """Decodificar un token."""
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            if payload and payload["scope"] == "access_token":
                return payload
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Scope for the token is invalid"
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    def encode_refresh_token(self, user) -> str:
        """Generar un token de actualización."""
        payload = {
            "exp": datetime.utcnow() + timedelta(hours=10),  # Token válido por 10 horas
            "iat": datetime.utcnow(),
            "scope": "refresh_token",
            "sub": user.email,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)
    
    def refresh_token(self, refresh_token: str) -> str:
        """Actualizar un token de acceso usando un token de actualización."""
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=[self.algorithm])
            if payload and payload["scope"] == "refresh_token":
                if self.db is None:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Database session not available"
                    )
                user = UserRepository(self.db).get_user_by_email(payload["sub"])
                return self.encode_token(user)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token"
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
    
    def encode_reset_token(self, user) -> str:
        """Generar un token de restablecimiento."""
        payload = {
            "sub": user["email"] if isinstance(user, dict) else user.email,
            "exp": datetime.utcnow() + timedelta(hours=1)  # Token válido por 1 hora
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)
    
    def verify_reset_token(self, token: str, email: str) -> bool:
        """Verificar un token de restablecimiento."""
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return payload["sub"] == email
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False