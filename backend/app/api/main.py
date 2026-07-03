import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.database.session import engine, Base

# Crear las tablas físicas en la base de datos al inicializar si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs"  # Habilita la documentación Swagger interactiva para el profesor
)

# Configuración estricta de CORS para comunicación local e inter-contenedores
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar a dominios específicos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar las rutas globales de la API V1
app.add_api_route(settings.API_V1_STR, api_router)

# Ruta base de salud del sistema
@app.get("/", tags=["Healthcheck"])
def root_healthcheck():
    return {"status": "online", "project": settings.PROJECT_NAME, "version": settings.VERSION}

if __name__ == "__main__":
    # Arrancar el servidor en modo desarrollo
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)