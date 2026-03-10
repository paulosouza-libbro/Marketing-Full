from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from tools.meta_integration import (
    get_page_info, get_page_insights, get_page_posts,
    get_instagram_insights, get_instagram_posts, get_resumo,
    publicar_facebook, publicar_instagram
)

router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("/status")
def status_meta():
    """Verifica conexão com Meta e retorna resumo da página e Instagram."""
    return get_resumo()


@router.get("/facebook/insights")
def insights_facebook(dias: int = 30):
    return get_page_insights(dias)


@router.get("/facebook/posts")
def posts_facebook(limit: int = 10):
    return get_page_posts(limit)


@router.get("/instagram/insights")
def insights_instagram(dias: int = 30):
    return get_instagram_insights(dias)


@router.get("/instagram/posts")
def posts_instagram(limit: int = 10):
    return get_instagram_posts(limit)


class PublicarFacebookRequest(BaseModel):
    mensagem: str
    link: Optional[str] = None


class PublicarInstagramRequest(BaseModel):
    imagem_url: str
    legenda: str


@router.post("/facebook/publicar")
def publicar_fb(body: PublicarFacebookRequest):
    result = publicar_facebook(body.mensagem, body.link)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"status": "publicado", "post_id": result.get("id")}


@router.post("/instagram/publicar")
def publicar_ig(body: PublicarInstagramRequest):
    result = publicar_instagram(body.imagem_url, body.legenda)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return {"status": "publicado", "media_id": result.get("id")}
