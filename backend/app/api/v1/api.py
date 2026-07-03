from fastapi import APIRouter
from app.api.v1.endpoints import dashboard, trends

api_router = APIRouter()

# Registramos los submódulos de forma limpia
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(trends.router, prefix="/trends", tags=["Trends"])