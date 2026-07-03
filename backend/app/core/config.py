import urllib.parse
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
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        # Codifica la contraseña para que ignore caracteres como '@' o '/'
        password_encoded = urllib.parse.quote_plus(self.DB_PASSWORD)
        
        # SI ESTÁS EN DESARROLLO LOCAL (Fuera de Docker), usamos SQLite automáticamente
        # para que puedas probar el backend sin levantar contenedores pesados aún.
        if self.DB_HOST == "db" and self.DB_USER == "generalAdmin":
            return "sqlite:///./opinionscope.db"
            
        # Cuando corra dentro de Docker, usará la URL real de Postgres
        return f"postgresql://{self.DB_USER}:{password_encoded}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()

settings = Settings()