from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 1. Crear el motor de conexión de SQLAlchemy
# pool_pre_ping=True ayuda a recuperar conexiones caídas automáticamente dentro de Docker
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# 2. Configurar la fábrica de sesiones independientes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Clase base de la que heredarán todos nuestros modelos ORM
Base = declarative_base()

def get_db() -> Generator:
    """ Dependencia para FastAPI que asegura la apertura y cierre de 
        sesiones por ciclo de petición de forma segura.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()