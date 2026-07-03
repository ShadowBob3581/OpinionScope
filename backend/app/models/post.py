from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, timezone
from app.database.session import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    red_social = Column(String(50), default="X (Twitter)", nullable=False)
    usuario = Column(String(100), nullable=False)
    texto = Column(String(500), nullable=False)
    
    # Métricas calculadas por el pipeline de IA (NLP)
    sentimiento = Column(String(20), nullable=False)  # Positivo, Negativo, Neutral
    nlp_confidence = Column(Float, nullable=False)     # Certeza del modelo (0.0 a 1.0)
    relevancia = Column(Float, nullable=False)         # Score de impacto (0.0 a 10.0)
    
    # Control de tiempo indexado para búsquedas ultrarrápidas
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True, nullable=False)