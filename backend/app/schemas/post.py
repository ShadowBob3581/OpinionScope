from pydantic import BaseModel, Field
from datetime import datetime

# Esqueleto común
class PostBase(BaseModel):
    red_social: str = "X (Twitter)"
    usuario: str
    texto: str = Field(..., min_length=1, max_length=500)

# Molde estricto para crear un registro tras el análisis de la IA
class PostCreate(PostBase):
    sentimiento: str = Field(..., description="Positivo, Negativo o Neutral")
    nlp_confidence: float = Field(..., ge=0.0, le=1.0)
    relevancia: float = Field(..., ge=0.0, le=10.0)

# Revisa que este nombre esté escrito idéntico, letra por letra:
class PostResponse(PostBase):
    id: int
    sentimiento: str
    nlp_confidence: float
    relevancia: float
    created_at: datetime

    # Permite a Pydantic leer directamente los objetos ORM de SQLAlchemy
    model_config = {"from_attributes": True}