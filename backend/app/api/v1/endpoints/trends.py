from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.post import Post
from app.schemas.post import PostResponse

router = APIRouter()

@router.get("/history", response_model=List[PostResponse])
def listar_historico_posts(
    sentimiento: Optional[str] = None,
    limit: int = Query(default=50, le=100),
    db: Session = Depends(get_db)
):
    """ Recupera el histórico de publicaciones procesadas con filtros avanzados 
        de sentimiento e índices temporales.
    """
    query = db.query(Post)
    if sentimiento:
        query = query.filter(Post.sentimiento == sentimiento)
    
    # Traer los más recientes primero aprovechando el índice en created_at
    return query.order_by(Post.created_at.desc()).limit(limit).all()