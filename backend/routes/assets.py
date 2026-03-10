"""
Rotas de assets por conto — upload e listagem.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from pathlib import Path
from datetime import datetime
import json, os, shutil

router = APIRouter(prefix="/contos", tags=["assets"])

ASSETS_PATH = Path(os.getenv("ASSETS_PATH", "../assets"))

ASSET_TIPOS = {
    "texto_original":   {"label": "Texto original do conto", "extensoes": [".txt", ".pdf", ".docx", ".md"], "icon": "📄"},
    "ilustracoes":      {"label": "Ilustrações do conto",    "extensoes": [".zip", ".jpg", ".png", ".pdf"], "icon": "🖼️"},
    "musicas":          {"label": "Músicas do conto",        "extensoes": [".mp3", ".wav", ".zip"],          "icon": "🎵"},
    "video_completo":   {"label": "Vídeo completo do conto", "extensoes": [".mp4", ".mov", ".mkv"],          "icon": "🎬"},
    "fonte":            {"label": "Fonte usada no conto",    "extensoes": [".ttf", ".otf", ".zip"],          "icon": "🔤"},
}


def assets_path_conto(slug: str) -> Path:
    return ASSETS_PATH / "ilustracoes-contos" / slug / "assets-fabrica"


def load_assets_meta(slug: str) -> dict:
    meta_path = assets_path_conto(slug) / "meta.json"
    if meta_path.exists():
        return json.loads(meta_path.read_text())
    # Retorna estrutura padrão com todos pendentes
    return {tipo: {"status": "pendente", "arquivo": None, "enviado_em": None} for tipo in ASSET_TIPOS}


def save_assets_meta(slug: str, meta: dict):
    path = assets_path_conto(slug)
    path.mkdir(parents=True, exist_ok=True)
    (path / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))


@router.get("/{slug}/assets")
def listar_assets(slug: str):
    """Retorna todos os assets do conto com status e metadados."""
    base = ASSETS_PATH / "ilustracoes-contos" / slug
    if not base.exists():
        raise HTTPException(status_code=404, detail="Conto não encontrado")

    meta = load_assets_meta(slug)
    resultado = []
    for tipo, info in ASSET_TIPOS.items():
        asset_meta = meta.get(tipo, {"status": "pendente", "arquivo": None, "enviado_em": None})
        resultado.append({
            "tipo": tipo,
            "label": info["label"],
            "icon": info["icon"],
            "extensoes_aceitas": info["extensoes"],
            "status": asset_meta["status"],
            "arquivo": asset_meta["arquivo"],
            "enviado_em": asset_meta["enviado_em"],
        })

    total = len(resultado)
    preenchidos = sum(1 for a in resultado if a["status"] == "preenchido")
    return {
        "conto": slug,
        "assets": resultado,
        "progresso": {"total": total, "preenchidos": preenchidos, "pct": int(preenchidos / total * 100)},
        "completo": preenchidos == total,
    }


@router.post("/{slug}/assets/{tipo}")
async def upload_asset(slug: str, tipo: str, arquivo: UploadFile = File(...)):
    """Faz upload de um asset para o conto."""
    base = ASSETS_PATH / "ilustracoes-contos" / slug
    if not base.exists():
        raise HTTPException(status_code=404, detail="Conto não encontrado")

    if tipo not in ASSET_TIPOS:
        raise HTTPException(status_code=400, detail=f"Tipo inválido. Use: {list(ASSET_TIPOS.keys())}")

    info = ASSET_TIPOS[tipo]
    ext = Path(arquivo.filename).suffix.lower()
    if ext not in info["extensoes"]:
        raise HTTPException(status_code=400, detail=f"Extensão {ext} não permitida para {tipo}. Use: {info['extensoes']}")

    # Salva arquivo
    dest_dir = assets_path_conto(slug)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / f"{tipo}{ext}"

    with open(dest_path, "wb") as f:
        shutil.copyfileobj(arquivo.file, f)

    # Atualiza meta
    meta = load_assets_meta(slug)
    meta[tipo] = {
        "status": "preenchido",
        "arquivo": str(dest_path.name),
        "enviado_em": datetime.now().isoformat(),
        "tamanho_bytes": dest_path.stat().st_size,
    }
    save_assets_meta(slug, meta)

    return {
        "status": "ok",
        "tipo": tipo,
        "label": info["label"],
        "arquivo": dest_path.name,
        "tamanho_kb": round(dest_path.stat().st_size / 1024, 1),
    }


@router.delete("/{slug}/assets/{tipo}")
def remover_asset(slug: str, tipo: str):
    """Remove um asset do conto."""
    if tipo not in ASSET_TIPOS:
        raise HTTPException(status_code=400, detail="Tipo inválido")

    dest_dir = assets_path_conto(slug)
    meta = load_assets_meta(slug)

    # Remove arquivo se existir
    if meta.get(tipo, {}).get("arquivo"):
        arquivo_path = dest_dir / meta[tipo]["arquivo"]
        if arquivo_path.exists():
            arquivo_path.unlink()

    meta[tipo] = {"status": "pendente", "arquivo": None, "enviado_em": None}
    save_assets_meta(slug, meta)

    return {"status": "removido", "tipo": tipo}
