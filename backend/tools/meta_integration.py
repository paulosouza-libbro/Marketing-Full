"""
Integração com Meta Business API (Facebook + Instagram).
"""
import os
import httpx
from datetime import datetime

BASE = "https://graph.facebook.com/v19.0"
PAGE_ID = os.getenv("META_PAGE_ID", "309268935596666")
PAGE_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
APP_ID = os.getenv("META_APP_ID", "")
APP_SECRET = os.getenv("META_APP_SECRET", "")


def _get(endpoint: str, params: dict = {}) -> dict:
    params["access_token"] = PAGE_TOKEN
    r = httpx.get(f"{BASE}/{endpoint}", params=params, timeout=15)
    return r.json()


def _post(endpoint: str, data: dict = {}) -> dict:
    data["access_token"] = PAGE_TOKEN
    r = httpx.post(f"{BASE}/{endpoint}", data=data, timeout=15)
    return r.json()


# ─── Página Facebook ──────────────────────────────────────────────────────────

def get_page_info() -> dict:
    return _get(PAGE_ID, {"fields": "id,name,fan_count,instagram_business_account"})


def get_page_insights(dias: int = 30) -> dict:
    metrics = "page_impressions,page_reach,page_engaged_users,page_fan_adds_unique"
    return _get(f"{PAGE_ID}/insights", {
        "metric": metrics,
        "period": "day",
        "since": int((datetime.now().timestamp()) - dias * 86400),
    })


def get_page_posts(limit: int = 10) -> dict:
    return _get(f"{PAGE_ID}/posts", {
        "fields": "id,message,created_time,likes.summary(true),comments.summary(true),shares",
        "limit": limit,
    })


def publicar_facebook(mensagem: str, link: str = None) -> dict:
    data = {"message": mensagem}
    if link:
        data["link"] = link
    return _post(f"{PAGE_ID}/feed", data)


# ─── Instagram ────────────────────────────────────────────────────────────────

def get_instagram_id() -> str | None:
    info = get_page_info()
    ig = info.get("instagram_business_account", {})
    return ig.get("id") if ig else None


def get_instagram_insights(dias: int = 30) -> dict:
    ig_id = get_instagram_id()
    if not ig_id:
        return {"error": "Instagram não conectado à página"}
    metrics = "impressions,reach,profile_views,follower_count"
    return _get(f"{ig_id}/insights", {
        "metric": metrics,
        "period": "day",
        "since": int((datetime.now().timestamp()) - dias * 86400),
    })


def get_instagram_posts(limit: int = 10) -> dict:
    ig_id = get_instagram_id()
    if not ig_id:
        return {"error": "Instagram não conectado à página"}
    return _get(f"{ig_id}/media", {
        "fields": "id,caption,media_type,timestamp,like_count,comments_count,impressions,reach",
        "limit": limit,
    })


def publicar_instagram(imagem_url: str, legenda: str) -> dict:
    """Publica imagem no Instagram (2 passos: criar container → publicar)."""
    ig_id = get_instagram_id()
    if not ig_id:
        return {"error": "Instagram não conectado à página"}

    # Passo 1: cria container
    container = _post(f"{ig_id}/media", {
        "image_url": imagem_url,
        "caption": legenda,
    })
    container_id = container.get("id")
    if not container_id:
        return {"error": "Falha ao criar container", "detalhes": container}

    # Passo 2: publica
    return _post(f"{ig_id}/media_publish", {"creation_id": container_id})


# ─── Resumo geral ─────────────────────────────────────────────────────────────

def get_resumo() -> dict:
    page = get_page_info()
    ig_id = get_instagram_id()
    posts_fb = get_page_posts(5)
    posts_ig = get_instagram_posts(5) if ig_id else {"data": []}

    return {
        "facebook": {
            "pagina": page.get("name"),
            "seguidores": page.get("fan_count", 0),
            "posts_recentes": len(posts_fb.get("data", [])),
        },
        "instagram": {
            "conectado": ig_id is not None,
            "ig_id": ig_id,
            "posts_recentes": len(posts_ig.get("data", [])),
        },
    }
