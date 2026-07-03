from pydantic import BaseModel
from datetime import datetime

# Esqueleto común para la agregación temporal
class TrendAggregatedBase(BaseModel):
    bucket_time: datetime
    total_posts: int
    count_positivo: int
    count_negativo: int
    count_neutral: int
    avg_relevancia: float

# Molde para la creación en las tareas de fondo
class TrendAggregatedCreate(TrendAggregatedBase):
    pass

# Molde optimizado para la respuesta de las gráficas
class TrendAggregatedResponse(TrendAggregatedBase):
    id: int

    model_config = {"from_attributes": True}

# Schema compuesto especial para los KPIs rápidos del Dashboard superior
class DashboardKpisResponse(BaseModel):
    total_publicaciones: int
    porcentaje_positivo: float
    porcentaje_negativo: float
    porcentaje_neutral: float
    indice_relevancia_promedio: float