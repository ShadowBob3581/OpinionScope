from sqlalchemy import Column, Integer, Float, DateTime
from app.database.session import Base

class TrendAggregated(Base):
    __tablename__ = "trends_aggregated"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # El bloque de tiempo exacto que representa este resumen (ej. 2026-07-02 14:00:00)
    bucket_time = Column(DateTime, unique=True, index=True, nullable=False)
    
    # Métricas consolidadas en ese bloque de tiempo
    total_posts = Column(Integer, default=0, nullable=False)
    count_positivo = Column(Integer, default=0, nullable=False)
    count_negativo = Column(Integer, default=0, nullable=False)
    count_neutral = Column(Integer, default=0, nullable=False)
    
    # Promedio del índice de relevancia en este bloque
    avg_relevancia = Column(Float, default=0.0, nullable=False)