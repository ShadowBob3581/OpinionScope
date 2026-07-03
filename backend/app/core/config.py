from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field

class Settings(BaseSettings):
    # Configuración de la App
    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "OpinionScope"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Base de Datos (Variables individuales)
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int = 5432
    
    # Propiedad computada matemática para armar la URL de SQLAlchemy automáticamente
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        # Si estás desarrollando local fuera de docker puedes usar sqlite, 
        # pero aquí ya se prepara para la arquitectura Postgres/MySQL de producción.
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Configuración de Seguridad
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Parámetros de la IA y API de X
    NLP_MODEL_NAME: str
    MIN_RELEVANCE_THRESHOLD: float = Field(default=5.0, ge=0.0, le=10.0)
    X_API_KEY: str
    X_API_SECRET_KEY: str
    X_BEARER_TOKEN: str

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()