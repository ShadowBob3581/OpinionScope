from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.post import Post
from app.schemas.post import PostResponse

router = APIRouter()

@router.get("/history", response_model=List[PostResponse])
def obtener_historial_tendencias(
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Recupera el historial cronológico de las publicaciones capturadas
    y analizadas por el pipeline de Inteligencia Artificial.
    """
    # Consulta optimizada ordenando por el ID más reciente
    posts = db.query(Post).order_by(Post.id.desc()).limit(limit).all()
    return posts