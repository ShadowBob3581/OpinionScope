import asyncio
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.session import get_db
from app.models.post import Post
from app.schemas.trend import DashboardKpisResponse
from app.services.scraper_agent import ScraperAgentService

router = APIRouter()

@router.get("/kpis", response_model=DashboardKpisResponse)
def obtener_kpis_dashboard(db: Session = Depends(get_db)):
    """ Calcula de forma matemática y optimizada los porcentajes de impacto 
        emocional y la relevancia promedio actual en la base de datos.
    """
    total = db.query(Post).count()
    if total == 0:
        return DashboardKpisResponse(
            total_publicaciones=0, porcentaje_positivo=0.0,
            porcentaje_negativo=0.0, porcentaje_neutral=0.0,
            indice_relevancia_promedio=0.0
        )
    
    # Agrupación eficiente por columna de sentimiento
    conteos = db.query(Post.sentimiento, func.count(Post.id)).group_by(Post.sentimiento).all()
    dict_conteos = {sentimiento: c for sentimiento, c in conteos}
    
    pos = dict_conteos.get("Positivo", 0)
    neg = dict_conteos.get("Negativo", 0)
    neu = dict_conteos.get("Neutral", 0)
    
    avg_relevancia = db.query(func.avg(Post.relevancia)).scalar() or 0.0

    return DashboardKpisResponse(
        total_publicaciones=total,
        porcentaje_positivo=round((pos / total) * 100, 1),
        porcentaje_negativo=round((neg / total) * 100, 1),
        porcentaje_neutral=round((neu / total) * 100, 1),
        indice_relevancia_promedio=round(avg_relevancia, 1)
    )

@router.websocket("/ws/live")
async def websocket_stream_live(websocket: WebSocket, db: Session = Depends(get_db)):
    """ Abre un canal persistente bidireccional que inyecta datos analizados 
        por la IA directamente a la UI de React en tiempo real.
    """
    await websocket.accept()
    try:
        while True:
            # 1. Ejecutar el pipeline de ingesta, IA y guardado en SQL
            nuevo_post = ScraperAgentService.ejecutar_ingesta_unitaria(db)
            
            # 2. Formatear el payload de salida JSON estructurado
            payload = {
                "id": nuevo_post.id,
                "usuario": nuevo_post.usuario,
                "texto": nuevo_post.texto,
                "sentimiento": nuevo_post.sentimiento,
                "confidence": nuevo_post.nlp_confidence,
                "relevancia": nuevo_post.relevancia,
                "created_at": nuevo_post.created_at.strftime("%H:%M:%S")
            }
            
            # 3. Empujar los datos de manera asíncrona hacia el cliente
            await websocket.send_json(payload)
            
            # Pausa controlada de 4 segundos antes de capturar el siguiente tweet
            await asyncio.sleep(4)
            
    except WebSocketDisconnect:
        # El frontend cerró la pestaña o recargó la página, cerramos el túnel limpiamente
        pass