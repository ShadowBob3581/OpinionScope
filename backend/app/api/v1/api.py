from fastapi import APIRouter
from app.api.v1.endpoints import dashboard, trends

api_router = APIRouter()

# Unificamos los submódulos colgándoles sus rutas semánticas REST
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard Real-Time"])
api_router.include_router(trends.router, prefix="/trends", tags=["Analítica Histórica"])