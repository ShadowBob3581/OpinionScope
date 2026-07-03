from datetime import datetime, timedelta, timezone
from typing import Any, Union
import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Configuración del contexto de hashing (Bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_contrasena(contrasena_plana: str, contrasena_hasheada: str) -> bool:
    """Compara una contraseña en texto plano con su hash almacenado."""
    return pwd_context.verify(contrasena_plana, contrasena_hasheada)

def obtener_hash_contrasena(contrasena: str) -> str:
    """Genera un hash seguro utilizando el algoritmo bcrypt."""
    return pwd_context.hash(contrasena)

def crear_token_acceso(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """Genera un JSON Web Token (JWT) firmado para la sesión del usuario."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt